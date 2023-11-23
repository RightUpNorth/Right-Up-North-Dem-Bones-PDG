# Work Item Configuration README

This README file describes the attributes used in the work item JSON configuration. Each attribute corresponds to a specific parameter in the PDG work item setup for a subprocess command.

## JSON Attributes

- `nBones`: Integer - The number of bones to be used in the process.
  - Example: `42`

- `nInitIters`: Integer - The number of iterations per initial cluster splitting.
  - Example: `10`

- `nIters`: Integer - The number of global iterations for the process.
  - Example: `5`

- `tolerance`: Double - The convergence tolerance. The process stops if the error relatively reduces less than this value in the number of consecutive iterations defined by `patience`.
  - Example: `0.001`

- `patience`: Integer - The convergence patience. Used in conjunction with `tolerance` to determine when to stop the process.
  - Example: `3`

- `nTransIters`: Integer - The number of transformation update iterations per global iteration.
  - Example: `2`

- `bindUpdate`: Integer - Determines if the bind pose should be updated (0=no update, 1=update joint positions, 2=regroup joints under one root).
  - Example: `1`

- `transAffine`: Double - The bone translations affinity soft constraint.
  - Example: `0.5`

- `transAffineNorm`: Double - The p-Norm for bone translations affinity.
  - Example: `1.5`

- `nWeightsIters`: Integer - The number of weight update iterations per global iteration.
  - Example: `4`

- `nnz`: Integer - The number of non-zero weights per vertex.
  - Example: `8`

- `weightsSmooth`: Double - The weights smoothness soft constraint.
  - Example: `0.05`

- `weightsSmoothStep`: Double - The step size for the weights smoothness.
  - Example: `0.01`

- `dbg`: Integer - The debug level for the process.
  - Example: `2`

## Usage

To use these configurations, replace the placeholder values with actual paths and numerical values relevant to your specific use case. The JSON file should be structured as shown in the example, with each attribute being a key-value pair within the `work_item` dictionary.
