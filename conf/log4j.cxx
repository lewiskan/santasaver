# Set root logger level to INFO and its only appender to A1.
log4j.rootLogger=WARN, A1

# A1 is set to be a ConsoleAppender.
log4j.appender.A1=org.apache.log4j.ConsoleAppender

# A1 uses PatternLayout.
log4j.appender.A1.layout=org.apache.log4j.PatternLayout
log4j.appender.A1.layout.ConversionPattern=%d{yy-MM-dd HH:mm:ss.SSS} %X{pname}:%X{pid} %-5p %l- %m%n
log4j.appender.A1.serverFileAppender=org.apache.log4j.RollingFileAppender

# Tweak the timestamp format so that it sorts easier
log4j.appender.A1.serverFileAppender.fileName=/tmp/santasaver.log
