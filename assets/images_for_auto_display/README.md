# Pictures that are used automatically

Placing a picture in one of the folders here is all it takes to use it: there is no list to edit. The folder is the picture's one tag.

| Folder | Where the pictures appear |
|---|---|
| `homepage/` | in the frame beside the banner text on the home page (screens wider than about 990 pixels), in file-name order |

More folders can be added later (for example `events/`, `news/` or `history/`) once a page is set up to use them. A folder no page uses has no effect.

## Naming a picture

`NN__what-the-picture-shows.jpg`, for example `02__researchers-in-the-control-room.jpg`.

* `NN__` is optional. It sets the order (pictures are shown in file-name order); leave it out if the order does not matter.
* What follows is the picture's description for people who cannot see it (its alt text), so describe what is in it: use words and hyphens, not `IMG_1234`.
* Use only lower-case letters, digits, hyphens and underscores, and a lower-case extension: `.jpg`, `.jpeg`, `.png` or `.webp`.

## Sizing

* About 1,200 to 1,600 pixels wide, and under about 300 KB, because the home page loads them all. Photographs shaped about 4:3 fit the frame best; other shapes are trimmed to fit.
* At most 6 pictures are used on the home page (the first 6 in file-name order).
* Photographs of people need their permission.

Run `python check_images.py` before committing: it lists the pictures and warns about names, sizes and shapes.

Do not use symbolic links to share a picture between folders: GitHub Pages does not support them and a site that contains one can fail to build. Copy the file instead (it costs nothing: Git stores identical files once).
