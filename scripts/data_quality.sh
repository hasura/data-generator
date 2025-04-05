#!/bin/bash

cd example

ddn subgraph init data_quality
ddn subgraph add --subgraph data_quality/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph data_quality/subgraph.yaml
ddn codemod rename-graphql-prefixes --graphql-type-name 'DataQuality_'
ddn connector init data_quality --hub-connector hasura/postgres -i
ddn connector introspect data_quality
ddn model add data_quality "data_quality*"
ddn relationship add data_quality "*"

ddn supergraph build local
ddn run docker-start

