"""Test cases for checker module."""

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from md_ref_checker.checker import ReferenceChecker

if TYPE_CHECKING:
    pass


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for tests."""
    # Change to the temporary directory for the duration of the test
    os.chdir(str(tmp_path))
    print(f"\nTemporary directory: {tmp_path}")
    return tmp_path


@pytest.fixture
def checker(temp_dir: Path) -> ReferenceChecker:
    """Create a ReferenceChecker instance."""
    checker = ReferenceChecker(str(temp_dir), debug=True)
    return checker


def test_check_single_file(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test checking a single file with valid and invalid references."""
    # Create test files
    (temp_dir / "doc1.md").write_text(
        """
Here's a valid reference [[doc2]]
And an invalid one [[nonexistent]]
Also a valid image ![[image.png]]
And an invalid image ![[missing.png]]
"""
    )
    (temp_dir / "doc2.md").write_text("Some content")
    (temp_dir / "image.png").touch()

    result = checker.check_file("doc1.md")

    # Check invalid references
    assert len(result.invalid_refs) == 2
    invalid_targets = {ref.target for ref in result.invalid_refs}
    assert invalid_targets == {"nonexistent", "missing.png"}


def test_check_directory(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test checking an entire directory."""
    # Create test files
    (temp_dir / "doc1.md").write_text(
        """
Reference to [[doc2]]
Invalid reference [[nonexistent]]
"""
    )
    (temp_dir / "doc2.md").write_text(
        """
Back reference to [[doc1]]
Image reference ![[image.png]]
"""
    )
    (temp_dir / "image.png").touch()
    (temp_dir / "unused.png").touch()

    result = checker.check_directory()

    # Check invalid references
    assert len(result.invalid_refs) == 1
    assert result.invalid_refs[0].target == "nonexistent"

    # Check unused images
    assert result.unused_images == {"unused.png"}

    # Check unidirectional links
    assert not result.unidirectional_links  # doc1 and doc2 reference each other


def test_unidirectional_links(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test detection of unidirectional links."""
    # Create test files
    (temp_dir / "doc1.md").write_text("Reference to [[doc2]]")
    (temp_dir / "doc2.md").write_text("No back reference")

    result = checker.check_directory()

    assert len(result.unidirectional_links) == 1
    assert result.unidirectional_links[0] == ("doc1.md", "doc2.md")


def test_ignore_patterns(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test that ignored files are not checked."""
    # Create .gitignore
    (temp_dir / ".gitignore").write_text(
        """
/ignored/
temp.md
"""
    )

    # Create test files
    (temp_dir / "doc.md").write_text(
        """
[[ignored/doc]]
[[temp]]
"""
    )
    (temp_dir / "ignored").mkdir()
    (temp_dir / "ignored/doc.md").write_text("Should be ignored")
    (temp_dir / "temp.md").write_text("Should be ignored")

    # Recreate checker to load ignore file
    checker = ReferenceChecker(str(temp_dir))
    result = checker.check_directory()

    # References to ignored files should be invalid
    assert len(result.invalid_refs) == 2


def test_nested_references(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of nested directory references."""
    # Create test directory structure
    (temp_dir / "dir1").mkdir()
    (temp_dir / "dir1/doc1.md").write_text(
        """
[[../dir2/doc2]]
[[doc3]]
"""
    )
    (temp_dir / "dir2").mkdir()
    (temp_dir / "dir2/doc2.md").write_text("Some content")
    (temp_dir / "dir1/doc3.md").write_text("Some content")

    result = checker.check_file("dir1/doc1.md")

    assert not result.invalid_refs  # All references should be valid


def test_cross_directory_references(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of references across different directories."""
    # Create test directory structure
    (temp_dir / "dir1/subdir1").mkdir(parents=True)
    (temp_dir / "dir2/subdir2").mkdir(parents=True)

    # Reference a file in another directory
    (temp_dir / "dir1/subdir1/source.md").write_text(
        """
Reference to [[../../dir2/subdir2/target]]
Reference to [[target]]
"""
    )
    (temp_dir / "dir2/subdir2/target.md").write_text("Target content")

    result = checker.check_file("dir1/subdir1/source.md")

    assert not result.invalid_refs  # Both reference styles should be valid


def test_image_references(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of image references."""
    # Create test files
    (temp_dir / "assets").mkdir()
    (temp_dir / "assets/image1.png").touch()
    (temp_dir / "assets/image2.jpg").touch()
    (temp_dir / "doc.md").write_text(
        """
![[assets/image1.png]]
![Regular markdown](assets/image2.jpg)
![[missing.png]]
"""
    )

    result = checker.check_file("doc.md")

    # Only missing.png should be reported as invalid
    assert len(result.invalid_refs) == 1
    assert result.invalid_refs[0].target == "missing.png"


def test_reference_with_heading(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of references with heading anchors."""
    # Create test files
    (temp_dir / "doc1.md").write_text(
        """
[[doc2#heading1]]
[[doc2#nonexistent]]
[[missing#heading]]
"""
    )
    (temp_dir / "doc2.md").write_text(
        """
# heading1
Some content
"""
    )

    result = checker.check_file("doc1.md")

    # Only missing#heading should be invalid
    # Note: We don't check if headings exist, only if files exist
    assert len(result.invalid_refs) == 1
    assert result.invalid_refs[0].target == "missing"


def test_reference_search_order(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test the order of searching for referenced files."""
    # Create test directory structure
    (temp_dir / "dir1/subdir").mkdir(parents=True)
    (temp_dir / "dir2").mkdir()

    # Create test files
    (temp_dir / "dir1/subdir/source.md").write_text(
        """
[[target]]  # Should find local target first
"""
    )
    (temp_dir / "dir1/subdir/target.md").write_text("Local target")
    (temp_dir / "dir2/target.md").write_text("Remote target")

    result = checker.check_file("dir1/subdir/source.md")
    assert not result.invalid_refs  # Should find the local target.md


def test_file_extension_handling(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of references with and without file extensions."""
    # Create test files
    (temp_dir / "doc.md").write_text("Content")
    (temp_dir / "script.py").write_text("print('hello')")
    (temp_dir / "data.json").write_text("{}")
    (temp_dir / "source.md").write_text(
        """
[[doc]]  # Should add .md
[[script.py]]  # Exact extension
[[data.json]]  # Exact extension
[[missing]]  # Invalid reference
![[doc]]  # Should add .md
![[script.py]]  # Exact extension
![[missing.txt]]  # Invalid reference
""".strip()
    )

    print("\nCreated files:")
    for file in temp_dir.glob("*"):
        print(f"  {file.relative_to(temp_dir)}")

    result = checker.check_file("source.md")

    print("\nInvalid references:")
    for ref in result.invalid_refs:
        print(f"  {ref}")

    # Only missing and missing.txt should be invalid
    assert len(result.invalid_refs) == 2
    invalid_targets = {ref.target for ref in result.invalid_refs}
    assert invalid_targets == {"missing", "missing.txt"}


def test_embed_vs_link_references(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test that both [[]] and ![[]] can reference any file type."""
    # Create test files with different extensions
    (temp_dir / "doc.md").write_text("Content")
    (temp_dir / "image.png").write_text("binary")
    (temp_dir / "data.json").write_text("{}")

    (temp_dir / "source.md").write_text(
        """
# Links
[[doc]]  # Link to markdown
[[image.png]]  # Link to image
[[data.json]]  # Link to data

# Embeds
![[doc]]  # Embed markdown
![[image.png]]  # Embed image
![[data.json]]  # Embed data
""".strip()
    )

    print("\nCreated files:")
    for file in temp_dir.glob("*"):
        print(f"  {file.relative_to(temp_dir)}")

    result = checker.check_file("source.md")

    print("\nInvalid references:")
    for ref in result.invalid_refs:
        print(f"  {ref}")

    # All references should be valid
    assert not result.invalid_refs

    # Verify reference types
    refs = list(
        checker.parser.parse_references(
            "source.md", (temp_dir / "source.md").read_text()
        )
    )
    assert len(refs) == 6

    # Links (is_embed=False)
    links = [ref for ref in refs if not ref.is_embed]
    assert len(links) == 3
    assert {ref.target for ref in links} == {"doc", "image.png", "data.json"}

    # Embeds (is_embed=True)
    embeds = [ref for ref in refs if ref.is_embed]
    assert len(embeds) == 3
    assert {ref.target for ref in embeds} == {"doc", "image.png", "data.json"}


def test_default_md_extension(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test that .md extension is added only when no extension is present."""
    # Create test files
    (temp_dir / "note.md").write_text("Content")
    (temp_dir / "source.md").write_text(
        """
[[note]]  # Should add .md
[[note.md]]  # Already has .md
![[note]]  # Should add .md
![[note.md]]  # Already has .md
""".strip()
    )

    print("\nCreated files:")
    for file in temp_dir.glob("*"):
        print(f"  {file.relative_to(temp_dir)}")

    result = checker.check_file("source.md")

    print("\nInvalid references:")
    for ref in result.invalid_refs:
        print(f"  {ref}")

    # All references should be valid
    assert not result.invalid_refs

    # Each reference should resolve to the same file
    refs = list(
        checker.parser.parse_references(
            "source.md", (temp_dir / "source.md").read_text()
        )
    )
    assert len(refs) == 4

    for ref in refs:
        resolved = checker._resolve_reference(ref)
        print(f"\nResolved {ref.target} -> {resolved}")
        assert resolved == "note.md"


def test_unused_images(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test detection of unused image files."""
    # Create test files
    (temp_dir / "assets").mkdir()
    (temp_dir / "assets/used1.png").touch()
    (temp_dir / "assets/used2.jpg").touch()
    (temp_dir / "assets/unused1.png").touch()
    (temp_dir / "assets/unused2.jpg").touch()

    # Create markdown files with references
    (temp_dir / "doc1.md").write_text(
        """
# Document 1
![[assets/used1.png]]  # Embed image
[[assets/used2.jpg]]   # Link to image
""".strip()
    )

    (temp_dir / "doc2.md").write_text(
        """
# Document 2
![](assets/used1.png)  # Standard MD image
""".strip()
    )

    # Test normal mode (default)
    result = checker.check_directory()
    assert result.unused_images == {
        "assets/unused1.png",
        "assets/unused2.jpg",
    }

    # Test strict mode
    strict_checker = ReferenceChecker(str(temp_dir), strict_image_refs=True)
    strict_result = strict_checker.check_directory()
    assert strict_result.unused_images == {
        "assets/unused1.png",
        "assets/unused2.jpg",
        "assets/used2.jpg",  # Not counted in strict mode because it's only linked
    }


def test_mixed_file_references(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of mixed file types and reference styles."""
    # Create various file types
    (temp_dir / "doc1.md").write_text("Content 1")
    (temp_dir / "doc2.md").write_text("Content 2")
    (temp_dir / "script.py").write_text("print('hello')")
    (temp_dir / "data.json").write_text("{}")
    (temp_dir / "image.png").touch()

    (temp_dir / "source.md").write_text(
        """
# Links (no content embedding)
[[doc1]]  # .md will be added
[[doc2.md]]
[[script.py]]
[[data.json]]
[[image.png]]

# Embeds (with content embedding)
![[doc1]]  # .md will be added
![[doc2.md]]
![[script.py]]
![[data.json]]
![[image.png]]
""".strip()
    )

    print("\nCreated files:")
    for file in temp_dir.glob("*"):
        print(f"  {file.relative_to(temp_dir)}")

    result = checker.check_file("source.md")

    print("\nInvalid references:")
    for ref in result.invalid_refs:
        print(f"  {ref}")

    # All references should be valid
    assert not result.invalid_refs

    # Verify reference types
    refs = list(
        checker.parser.parse_references(
            "source.md", (temp_dir / "source.md").read_text()
        )
    )
    assert len(refs) == 10

    # First 5 should be links, last 5 should be embeds
    assert all(not ref.is_embed for ref in refs[:5])
    assert all(ref.is_embed for ref in refs[5:])


def test_image_reference_resolution(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test resolution of image references in different locations."""
    # Create test directory structure
    (temp_dir / "assets").mkdir()
    (temp_dir / "dir1").mkdir()
    (temp_dir / "dir1/assets").mkdir()

    # Create test files
    (temp_dir / "assets/image1.png").touch()
    (temp_dir / "dir1/assets/image2.png").touch()
    (temp_dir / "dir1/local_image.png").touch()

    # Test cases for different image reference locations
    test_cases = [
        # Reference from root directory
        ("doc1.md", "![[image1.png]]", "assets/image1.png"),
        ("doc1.md", "![[assets/image1.png]]", "assets/image1.png"),
        # Reference from subdirectory
        ("dir1/doc2.md", "![[image1.png]]", "assets/image1.png"),
        ("dir1/doc2.md", "![[../assets/image1.png]]", "assets/image1.png"),
        ("dir1/doc2.md", "![[assets/image2.png]]", "dir1/assets/image2.png"),
        ("dir1/doc2.md", "![[local_image.png]]", "dir1/local_image.png"),
    ]

    for source_file, content, expected_path in test_cases:
        # Create source file
        (temp_dir / source_file).write_text(content)

        # Check references
        result = checker.check_file(source_file)

        # Verify no invalid references
        assert not result.invalid_refs, f"Failed for {source_file}: {content}"

        # Verify image is tracked
        assert (
            expected_path in checker.image_refs
        ), f"Image not tracked: {expected_path}"


def test_image_reference_with_spaces(checker: ReferenceChecker, temp_dir: Path) -> None:
    """Test handling of image references with spaces in names."""
    # Create test files
    (temp_dir / "assets").mkdir()
    (temp_dir / "assets/my image.png").touch()
    (temp_dir / "doc with spaces.md").write_text("![[my image.png]]")

    result = checker.check_file("doc with spaces.md")
    assert not result.invalid_refs
    assert "assets/my image.png" in checker.image_refs
