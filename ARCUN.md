# WordCraft for Arcun

This branch is WordCraft (storytold/wordcraft, Apache-2.0 OR MIT) at the release tag it is named
after, with the changes below for Arcun, which frames WordCraft's web build in its own page
(`?host=parent`). Everything else is upstream's. The release workflow
(`.github/workflows/arcun-web.yml`) publishes the official web bundle of the base release with only
the built files (`index.html`, the JavaScript, the WebAssembly module, `snippets/`) replaced.

## Changes

- **`?chrome=notitlebar`**: a host page that shows the document's title and handles its files
  itself hides the title bar (AutoSave, title, search, account). Save, Undo and Redo move to the
  start of the tab strip; the menu that customizes them is left out. Only with a host bridge, only
  for this visit, never stored.
- **`?chrome=noshare`**: the tab strip's Share button is hidden for a host page that shares
  documents itself.
- **`document.snapshot`** in the control and page API (`window.wordcraft.request("document.snapshot")`):
  the document as Save would write it (`name`, `bytes`, base64 `data`, `dirty`), without saving. The
  unsaved flag, the revision, the file name and the undo history stay as they are, and the host page
  gets no save message. A host keeps it as its own draft of unsaved changes.

GridCraft has the same title bar parameter (storytold/wordcraft#4945 asks for it in WordCraft). The
changes are meant to be offered upstream; once upstream has them, this branch is no longer needed.

## Building

From `apps/wordcraft-web`, with storytold/craft-i18n at `craft-i18n.rev` and storytold/craft-fonts
at the commit the workflow names:

```sh
CRAFT_FONTS_DIR=../../../craft-fonts CRAFT_I18N_DIR=../../../craft-i18n CRAFT_I18N_REQUIRED=1 trunk build --release
```
