ddn context set subgraph consumer_banking/subgraph.yaml
ddn connector introspect consumer_banking
ddn model add consumer_banking "consumer_banking*"
ddn relationship add consumer_banking "*"

ddn context set subgraph consumer_lending/subgraph.yaml
ddn connector introspect consumer_lending
ddn model add consumer_lending "consumer_lending*"
ddn relationship add consumer_lending "*"

ddn context set subgraph mortgage_services/subgraph.yaml
ddn connector introspect mortgage_services
ddn model add mortgage_services "mortgage_services*"
ddn relationship add mortgage_services "*"

ddn context set subgraph mortgage_services/subgraph.yaml
ddn connector introspect mortgage_services
ddn model add mortgage_services "mortgage_services*"
ddn relationship add mortgage_services "*"

ddn context set subgraph credit_cards/subgraph.yaml
ddn connector introspect credit_cards
ddn model add credit_cards "credit_cards*"
ddn relationship add credit_cards "*"

ddn context set subgraph small_business_banking/subgraph.yaml
ddn connector introspect small_business_banking
ddn model add small_business_banking "small_business_banking*"
ddn relationship add small_business_banking "*"

ddn supergraph build local
ddn run docker-start
ddn console --local
