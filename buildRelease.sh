#!/bin/bash
(cd ../../; python2 ./generator.pyc hs_kostalInverterModbusTCP utf-8)
markdown2 --extras tables,fenced-code-blocks,strike,target-blank-links doc/log14180.md > release/log14180.html
(cd release; zip -r 14180_kostalInverterModbusTCP.hslz *)
