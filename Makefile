script-build-network-run: ./scripts/python/build_interaction_network.py
	@echo "Running build_interaction_network script..."
	@python3 ./scripts/python/build_interaction_network.py -i ./data/raw/clean_dialog.csv -o ./data/interim/dialog_network.json

script-build-network-help: ./scripts/python/build_interaction_network.py
	@python3 ./scripts/python/build_interaction_network.py -h

script-compute_network-run: ./scripts/python/compute_network_stats.py
	@echo "Running compute_network_stats script..."
	@python3 ./scripts/python/compute_network_stats.py -i ./data/interim/dialog_network.json -o ./data/processed/network_stats.json

script-compute_network-help: ./scripts/python/compute_network_stats.py
	@python3 ./scripts/python/compute_network_stats.py -h
