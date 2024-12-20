from pathlib import Path


def extract_webp_images(
    file_name: Path, tiles: list[tuple[int, int, int]], output_dir: Path
):
    with open(file_name, "rb") as f:
        data = f.read()

    output_dir.mkdir(exist_ok=True)

    offset = 0
    count = 0

    while True:
        # Find the WebP signature (RIFF....WEBP)
        offset = data.find(b"RIFF", offset)

        if offset == -1:
            break

        # Extract WebP size from the header (4 bytes after 'RIFF')
        size = int.from_bytes(data[offset + 4 : offset + 8], "little") + 8

        # Extract WebP image data
        webp_data = data[offset : offset + size]

        # Save to a file
        z, x, y = tiles[count]
        output_path = Path(f"{output_dir}/{z}_{x}_{y}.webp")

        with open(output_path, "wb") as f:
            f.write(webp_data)

        count += 1
        offset += size

    print(f"Extracted {count} WebP images to {output_dir}")
