# Tools & Libraries Used in tref

`tref` leverages a modern Python and JavaScript toolchain for both its CLI and website.

## Python (Backend/CLI)

- **Python 3.8+**: Main programming language
- **[torch](https://pytorch.org/)**: For tensor operations and running transformer models
- **[transformers](https://huggingface.co/docs/transformers/)**: For loading and using state-of-the-art language models (e.g., BAAI/bge-small-en-v1.5)
- **[numpy](https://numpy.org/)**: For fast numerical operations and similarity search
- **[argparse](https://docs.python.org/3/library/argparse.html)**: For CLI argument parsing
- **[pathlib](https://docs.python.org/3/library/pathlib.html)**: For cross-platform file and path management

## JavaScript/TypeScript (Website)

- **React**: UI library for building the website
- **TypeScript**: Type safety for React components
- **Vite**: Fast development server and build tool
- **Tailwind CSS**: Utility-first CSS framework for styling
- **lucide-react**: Icon library for modern SVG icons
- **react-router-dom**: Routing for single-page app navigation
- **@tanstack/react-query**: Data fetching and caching (if used)

## Other

- **JSON**: Cheat sheets are stored as JSON files for easy editing and portability
- **Markdown**: Documentation is written in Markdown and rendered on the website

---

For more, see the [Architecture](./architecture.md) and [Interface/Commands](./interface.md). 