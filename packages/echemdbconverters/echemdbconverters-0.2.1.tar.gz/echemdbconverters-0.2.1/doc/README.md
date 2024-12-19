# Sphinx Documentation of echemdb-unitpackage

This documentation is automatically built and uploaded to GitHub Pages.

To build and see the documentation locally, type:

```sh
cd doc
make html
python -m http.server 8880 -b localhost --directory generated/html &
```

Then open http://localhost:8880/ with your browser.

The build requires internet access, since data is pulled from
external repositories to evaluate the documentation content.
