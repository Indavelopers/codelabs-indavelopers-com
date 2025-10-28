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

### Using GCS

- Create 2 GCS buckets, one for staging and one for production:
  - Follow the how-to guide: <https://docs.cloud.google.com/storage/docs/hosting-static-website>
  - Set an appropiate regional or multi-regional location
  - Have an uniform level access
  - Assign public access giving the Storage Object Viewer access to allUsers
  - Issue CNAME redirects for the subdomains to `c.storage.googleapis.com`

### Authoring

- Write codelabs as markdown files in `tools/site/codelabs`
  - `codelabs` has a symlink to `tools/site/codelabs`
- Serve locally with Gulp in `tools/site`: `gulp serve`
  - Codelabs dir can be included as `gulp serve --codelabs-dir=codelabs`

### Deployment

- Export codelabs from `codelabs`:
  - Move to repo root dir, not `tools/site/codelabs`: from `tools/site`, run `../..`
- Export to HTML with CLaaT: `./claat export -o codelabs codelabs/*.md`
  - CLaaT is in the root dir
  - You can also export individual codelabs with `./claat -o codelabs codelabs/codelab_md_file.md`
  - You can export codelabs to a different output directory with `./claat -o output_dir codelabs/*.md`
- Deploy to eg. GCS: --> See quick fix below instead!
  - Setup envars with GCS staging bucket: `export STAGING_BUCKET=gs://codelabs-staging.indavelopers.com`
  - Same for GCS production bucket: `export PROD_BUCKET=gs://codelabs.indavelopers.com`
  - Compile and minify: `gulp dist`
  - Deploy to staging:
    - Deploy views: `gulp publish:staging:views --base-url=https://codelabs-staging.indavelopers.com --staging-bucket=$STAGING_BUCKET`
    - Deploy codelabs: `gulp publish:staging:codelabs --base-url=https://codelabs-staging.indavelopers.com --staging-bucket=$STAGING_BUCKET`
  - Deploy to production:
    - Deploy views: `gulp publish:prod:views --base-url=https://codelabs.indavelopers.com --staging-bucket=$STAGING_BUCKET --prod-bucket=$PROD_BUCKET`
    - Deploy codelabs: `gulp publish:prod:codelabs --base-url=https://codelabs.indavelopers.com --staging-bucket=$STAGING_BUCKET --prod-bucket=$PROD_BUCKET`

#### Gulp dist fix

- Currently, `gulp dist` produces some bugs regarding styles
- Current fix is to use `gulp serve` to create the `build` folder, then rsyncing this directly to GCS `gcloud storage rsync -r build/ $STAGING_BUCKET`

## Gulp postcss fix

When doing `gulp dist`, there's an error in `gulp-postcss` with an invalid `alphabetically` order value.

Change `tools/site/helpers/opts.js` line 33 to:

```javascript
cssdeclarationsorter({ order: 'alphabetical' }),
```

## License

See `LICENSE.md`
