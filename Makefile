videos/%.mov : code/%.py
	rm -rf frames/$(basename $< .py)
	mkdir -p frames/$(basename $< .py)
	python $<
	ffmpeg -qscale 5 -r 20 -b 9600 -i frames/$(basename $< .py)/frame%04d.png $@

presentation.key : presentation_template.key videos/*.mov
	mkdir presentation_contents
	cp presentation_template.key presentation.key
	cd videos && zip *.mov ../presentation.key

clean :
	rm -rf frames
	rm -rf videos
	rm -f presentation.key

all : presentation.key

.PHONY = all clean
