### Videos go here ###
VIDEO_NAMES = cat wind push
VIDEO_SUFFIX = .mov

# Everything else can remain untouched:

VIDEOS = $(addsuffix $(VIDEO_SUFFIX),$(addprefix videos/,$(VIDEO_NAMES)))

all : $(VIDEOS)

videos : 
	mkdir -p videos

videos/%.mov : code/%.py videos code/helpers/*
	$(eval NAME=$(notdir $<))
	$(eval FILENAME=$(basename $(NAME) .py))
	rm -rf frames/$(FILENAME)
	mkdir -p frames/$(FILENAME)
	cd frames/$(FILENAME) && python $(abspath $<)
	ffmpeg -y -r 60 -i $(addsuffix /frame%04d.bmp,frames/$(FILENAME)) -vcodec qtrle -pix_fmt argb $@

$(VIDEO_NAMES) : $(VIDEOS)
	open videos/$@$(VIDEO_SUFFIX)

clean :
	rm -rf frames
	rm -rf videos

.PHONY = all clean
