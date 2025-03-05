mkdir example
cd example

ddn supergraph init .
ddn project init

ddn subgraph init consumer_banking
ddn subgraph add --subgraph consumer_banking/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph consumer_banking/subgraph.yaml
# shellcheck disable=SC1110
ddn codemod rename-graphql-prefixes --graphql-type-name 'ConsumerBanking_'
ddn connector init consumer_banking --hub-connector hasura/postgres -i
ddn connector introspect consumer_banking
ddn model add consumer_banking "consumer_ddn model add consumer_banking "consumer_banking*"banking*"
ddn relationship add consumer_banking "*"

ddn subgraph init consumer_lending
ddn subgraph add --subgraph consumer_lending/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph consumer_lending/subgraph.yaml
ddn codemod rename-graphql-prefixes --graphql-type-name 'ConsumerLending'
ddn connector init consumer_lending --hub-connector hasura/postgres -i
ddn connector introspect consumer_lending
ddn model add consumer_lending "consumer_lending*"
ddn relationship add consumer_lending "*"

ddn subgraph init mortgage_services
ddn subgraph add --subgraph mortgage_services/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph mortgage_services/subgraph.yaml
ddn codemod rename-graphql-prefixes --graphql-type-name 'MortgageServices_'
ddn connector init mortgage_services --hub-connector hasura/postgres -i
ddn connector introspect mortgage_services
ddn model add mortgage_services "mortgage_services*"
ddn relationship add mortgage_services "*"

ddn subgraph init mortgage_services
ddn subgraph add --subgraph mortgage_services/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph mortgage_services/subgraph.yaml
ddn codemod rename-graphql-prefixes --graphql-type-name 'MortgageServices_'
ddn connector init mortgage_services --hub-connector hasura/postgres -i
ddn connector introspect mortgage_services
ddn model add mortgage_services "mortgage_services*"
ddn relationship add mortgage_services "*"

ddn subgraph init credit_cards
ddn subgraph add --subgraph credit_cards/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph credit_cards/subgraph.yaml
ddn codemod rename-graphql-prefixes --graphql-type-name 'CreditCards_'
ddn connector init credit_cards --hub-connector hasura/postgres -i
ddn connector introspect credit_cards
ddn model add credit_cards "credit_cards*"
ddn relationship add credit_cards "*"

ddn subgraph init small_business_banking
ddn subgraph add --subgraph small_business_banking/subgraph.yaml --target-supergraph ./supergraph.yaml
ddn context set subgraph small_business_banking/subgraph.yaml
ddn codemod rename-graphql-prefixes --graphql-type-name 'SmallBusinessBanking_'
ddn connector init small_business_banking --hub-connector hasura/postgres -i
ddn connector introspect small_business_banking
ddn model add small_business_banking "small_business_banking*"
ddn relationship add small_business_banking "*"

ddn supergraph build local
ddn codemode enable-promptql
ddn run docker-start
ddn console --local
