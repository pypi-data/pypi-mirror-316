# langchain-yt-dlp

**`langchain-yt-dlp`** is a Python package that extends [LangChain](https://github.com/langchain-ai/langchain) by providing an improved YouTube integration using `yt-dlp`.
This package addresses a critical limitation in the existing LangChain YoutubeLoader. The original implementation, which relied on `pytube`, became unable to fetch YouTube metadata due to changes in YouTube's structure. `langchain-yt-dlp` resolves this by leveraging the robust `yt-dlp` library, providing a more reliable YouTube document loader.

---

## Key Features

- Retrieve metadata (e.g., title, description, author, view count, publish date) using the `yt-dlp` library.
- Maintain compatibility with LangChain's existing loader interface.

---

## Installation

To install the package, use:

```bash
pip install langchain-yt-dlp
```

Ensure you have the following dependencies installed:
- `langchain`
- `yt-dlp`

Install them with:
```bash
pip install langchain yt-dlp
```

---

## Usage

Here’s how you can use the `YoutubeLoader` from `langchain-yt-dlp`:

### **Basic Example**



### **Loading From a YouTube URL**

```python
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL

# Initialize using a YouTube URL
loader = YoutubeLoaderDL.from_youtube_url(
    youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
    add_video_info=True
)

documents = loader.load()
print(documents)
```

---

## Parameters

### `YoutubeLoader` Constructor

| Parameter      | Type | Default | Description                             |
|----------------|------|---------|-----------------------------------------|
| `video_id`       | `str`  | None    | The YouTube video ID to fetch data for. |
| `add_video_info` | `bool` | `False`   | Whether to fetch additional metadata.   |

---

## Testing

To run the tests:

1. Clone the repository:
   ```bash
   git clone https://github.com/aqib0770/langchain-yt-dlp
   cd langchain-yt-dlp
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests:
   ```bash
   pytest tests/test_youtube_loader.py
   ```

---

## Contributing

Contributions are welcome! If you have ideas for new features or spot a bug, feel free to:
- Open an issue on [GitHub](https://github.com/aqib0770/langchain-yt-dlp/issues).
- Submit a pull request.


---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/aqib0770/langchain-yt-dlp/blob/main/LICENSE) file for details.

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for providing the base integration framework.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for enabling enhanced YouTube metadata extraction.
