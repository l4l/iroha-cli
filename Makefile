all:
	python -m grpc_tools.protoc -Ischema --python_out=. --grpc_python_out=. schema/*.proto
