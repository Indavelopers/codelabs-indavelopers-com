# codelabs-indavelopers-com

Public codelabs including tutorials and workshops in [codelabs.indavelopers.com](https://codelabs.indavelopers.com)

It makes use of CLaaT or codelabs tools available at: <https://github.com/googlecodelabs/tools>

Best tutorial for CLaaT by @zarinlo: <https://medium.com/@zarinlo/publish-technical-tutorials-in-google-codelab-format-b07ef76972cd>

## Maintainer

Marcos Manuel Ortega: <info@indavelopers.com>
Consultant, architect and trainer
Google Cloud Authorized Trainer
Google Developer Expert
LinkedIn: [Marcos Manuel Ortega](https://www.linkedin.com/in/marcosmanuelortega/)

## Instructions

### Installation

- Clone @zarinlo fork instead with fixes till her [PR](https://github.com/googlecodelabs/tools/pull/915) is merged: `git clone https://github.com/zarinlo/tools.git`
- Install Gulp and dependencies, as per @zarinlo tutorial in `tools/site`: `npm install`, `npm install -g gulp-cli`
- Install CLaaT, move to root dir as `claat`
- Make CLaaT executable as `chmod u+x claat`

### Authoring

- Write codelabs as markdown files in `tools/site/codelabs`
  - `codelabs` has a symlink to `tools/site/codelabs`
- Serve locally with Gulp in `tools/site`: `gulp serve`
  - Codelabs dir can be included as `gulp serve --codelabs-dir=codelabs`

### Deployment

- Export codelabs from `codelabs`:
  - Move to repo root dir, not `tools/site/codelabs`: from `tools/site`, run `../..`
- Export to HTML with CLaaT: `./claat export codelabs/*.md`
  - CLaaT is in the root dir
  - You can also export individual codelabs with `./claat codelabs/codelab_md_file.md`
- Deploy to eg. GCS:
  - TODO

## License

See `LICENSE.md`
