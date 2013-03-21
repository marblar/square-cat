### Videos go here ###
VIDEO_NAMES = test
VIDEO_SUFFIX = .mov

# Everything else can remain untouched:

VIDEOS = $(addsuffix $(VIDEO_SUFFIX),$(addprefix videos/,$(VIDEO_NAMES)))

all : presentation.key

videos : 
	mkdir -p videos

videos/%.mov : code/%.py videos
	$(eval NAME=$(notdir $<))
	$(eval FILENAME=$(basename $(NAME) .py))
	rm -rf frames/$(FILENAME)
	mkdir -p frames/$(FILENAME)
	cp $< frames/$(FILENAME)
	cd frames/$(FILENAME) && env SDL_VIDEODRIVER=dummy python $(NAME)
	ffmpeg -y -f image2 -r 60 -i $(addsuffix /frame%04d.png,frames/$(FILENAME)) -vcodec qtrle -pix_fmt rgb24 $@

presentation.key : presentation_template.key $(VIDEOS) modify_apxl.py
	unzip -o presentation_template.key -d contents
	python modify_apxl.py
	cp videos/* contents/ 
	cd contents && zip ../presentation.key *

$(VIDEO_NAMES) : $(VIDEOS)
	open videos/$@$(VIDEO_SUFFIX)

clean :
	rm -rf contents
	rm -rf frames
	rm -rf videos
	rm -f presentation.key

all : presentation.key

.PHONY = all clean
