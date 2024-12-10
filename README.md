# Quickstart

1. Install docker
2. Obtain the propert env variables and create a .env file containing them
3. run `docker build .`
4. run `docker-compose up dev` to develop
5. run `docker-compose up build` to build (outputs to `dist` folder)

## Latest Test Results
The expected deviation from default data is shown as a percentage.

<!-- LATEST TEST HERE -->

| Test Name | Deviation |
|-----------|-----------|
| 2022 County Totals :: SUM_LBS_CHEMICAL | 0.077% |
| 2022 County Totals :: SUM_LBS_PRODUCT | 0.531% |
| 2022 County correlation :: SUM_LBS_CHEMICAL r-squared | 100.0 |
| 2022 County correlation :: SUM_LBS_PRODUCT r-squared | 99.957 |
| 2020 County ag totals :: SUM_LBS_CHEMICAL | 0.06% |
| 2020 County ag totals :: SUM_LBS_PRODUCT | 0.084% |
| 2020 County ag correlation :: SUM_LBS_CHEMICAL r-squared | 100.0 |
| 2020 County ag correlation :: SUM_LBS_PRODUCT r-squared | 100.0 |
| 2022 County non-ag totals :: SUM_LBS_CHEMICAL | 0.109% |
| 2022 County non-ag totals :: SUM_LBS_PRODUCT | 0.664% |
| 2022 County non-ag correlation :: SUM_LBS_CHEMICAL r-squared | 99.999 |
| 2022 County non-ag correlation :: SUM_LBS_PRODUCT r-squared | 98.286 |
| Tract Sum Total SUM_LBS_CHEMICAL | 0.1% |
| Tract Sum Total SUM_LBS_PRODUCT | 0.144% |
| School Districts Sum Total SUM_LBS_CHEMICAL | 0.1% |
| School Districts Sum Total SUM_LBS_PRODUCT | 0.144% |
| ZCTA Sum Total SUM_LBS_CHEMICAL | -1.914% |
| ZCTA Sum Total SUM_LBS_PRODUCT | -2.099% |
| Townships Total SUM_LBS_CHEMICAL | 0.1% |
| Townships Total SUM_LBS_PRODUCT | 0.144% |
| Section Total SUM_LBS_CHEMICAL | 0.1% |
| Section Total SUM_LBS_PRODUCT | 0.144% |
| Sections Sacramento alfalfa total POUNDS_CHEMICAL_APPLIED | -0.0% |
| Sections Sacramento alfalfa total POUNDS_PRODUCT_APPLIED | -0.027% |
| Sections Sacramento alfalfa correlation :: POUNDS_CHEMICAL_APPLIED r-squared | 100.0 |
| Sections Sacramento alfalfa correlation :: POUNDS_PRODUCT_APPLIED r-squared | 100.0 |
<!-- END LATEST TEST -->
## env requirements
```
VITE_DATA_ENDPOINT = ... // Open Spatial Lab NECTR endpoint
VITE_MAPBOX_TOKEN = ... // mapbox API key

```

## Output
In `dist` after running the build, you'll find a folder, `assets`, containing the relevant code chunks and graphics. Deploy this on your website and add the minimal HTML from `index.html` to your desired page. 

## Github Actions to Build the application
Alternatively to Docker, you can use github actions to build the application:
1. From the repository, go to "Actions" on the repo menu
2. Go to "Build Vite Application" on the left hand pane
3. Click "Run Workflow" > "Run Workflow"
4. After the build completes, looks for the section titled "Artifacts" at the bottom of the action run information. Download the artifact "dist" which contains the build output

# Boilerplate: React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default {
  // other rules...
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
    tsconfigRootDir: __dirname,
  },
}
```

- Replace `plugin:@typescript-eslint/recommended` to `plugin:@typescript-eslint/recommended-type-checked` or `plugin:@typescript-eslint/strict-type-checked`
- Optionally add `plugin:@typescript-eslint/stylistic-type-checked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and add `plugin:react/recommended` & `plugin:react/jsx-runtime` to the `extends` list
