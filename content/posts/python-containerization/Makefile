# Shortcuts for building the images for this article

.PHONY: all clean one

all:

	@echo "Building all images..."
	$(MAKE) clean
	$(MAKE) one
	$(MAKE) clean
	$(MAKE) two
	$(MAKE) clean
	$(MAKE) three
	$(MAKE) clean
	$(MAKE) four
	$(MAKE) clean
	$(MAKE) five
	$(MAKE) clean
	$(MAKE) six
	@echo "Done!"

clean:

	@echo "Clearing all Docker data..."
	docker system prune -af
	@echo "Done!"

one:

	@echo "Building Docker image for take one..."
	docker build -f take_1/Dockerfile -t take_one:latest .
	@echo "Done with take one image!"

two:

	@echo "Building Docker image for take two..."
	docker build -f take_2/Dockerfile -t take_two:latest .
	@echo "Done with take two image!"

three:

	@echo "Building Docker image for take three..."
	docker build -f take_3/Dockerfile -t take_three:latest .
	@echo "Done with take three image!"

four:

	@echo "Building Docker image for take four..."
	docker build -f take_4/Dockerfile -t take_four:latest .
	@echo "Done with take four image!"

five:

	@echo "Building Docker image for take five..."
	docker build -f take_5/Dockerfile -t take_five:latest .
	@echo "Done with take five image!"

six:

	@echo "Building Docker image for take six..."
	docker build -f take_6/Dockerfile -t take_six:latest .
	@echo "Done with take six image!"