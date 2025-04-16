#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Score predictions file

requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
    - entryname: score.py
      entry: |
        #!/usr/bin/env python
        import argparse
        import json
        from synapseclient import Synapse as syn
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--submissionfile", required=True, help="Submission File")
        parser.add_argument("-r", "--results", required=True, help="Scoring results")
        parser.add_argument("-g", "--goldstandard", required=True, help="Goldstandard for scoring")
        parser.add_argument("-s", "--submissionid", required=True, help="Submission ID")

        args = parser.parse_args()
        score = 1 + 1
        prediction_file_status = "SCORED"
        
        syn = syn()
        status = syn.getSubmissionStatus(args.submissionid)
        status.score = score
        status.status = 'SCORED'
        status = syn.store(status)

        result = {'auc': args.submissionfile,
                  'submission_status': prediction_file_status}
        with open(args.results, 'w') as o:
          o.write(json.dumps(result))

inputs:
  - id: input_file
    type: File
  - id: goldstandard
    type: File
  - id: check_validation_finished
    type: boolean?
  - id: submissionid
    type: int

outputs:
  - id: results
    type: File
    outputBinding:
      glob: results.json
  - id: status
    type: string
    outputBinding:
      glob: results.json
      outputEval: $(JSON.parse(self[0].contents)['submission_status'])
      loadContents: true

baseCommand: python
arguments:
  - valueFrom: score.py
  - prefix: -f
    valueFrom: $(inputs.input_file.path)
  - prefix: -g
    valueFrom: $(inputs.goldstandard.path)
  - prefix: -r
    valueFrom: results.json
  - prefix: -s
    valueFrom: $(inputs.submissionid)

hints:
  DockerRequirement:
    dockerPull: python:3.9.1-slim-buster
