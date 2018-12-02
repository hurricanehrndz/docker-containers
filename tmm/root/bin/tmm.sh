#!/bin/bash

java -classpath tmm.jar:lib/* \
  -Dcom.threerings.getdown=true \
  -XX:+IgnoreUnrecognizedVMOptions \
  --add-modules=java.xml.bind \
  --add-modules=java.xml.ws \
  -Xms64m \
  -Xmx256m \
  -Xss512k \
  -splash:splashscreen.png \
  -Djava.net.preferIPv4Stack=true \
  -Dfile.encoding=UTF-8 \
  -XX:CompileCommand=exclude,ca/odell/glazedlists/impl/filter/TextMatchers,matches \
  -XX:CompileCommand=exclude,ca/odell/glazedlists/impl/filter/BoyerMooreCaseInsensitiveTextSearchStrategy,indexOf \
  -Djna.nosys=true \
  org.tinymediamanager.TinyMediaManager
