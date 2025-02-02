FROM openjdk:8-jdk-alpine VOLUME /tmp ARG JAVA_OPTS 
ENV JAVA_OPTS=$JAVA_OPTS COPY lyceoaiproject.jar 
lyceoaiproject.jar EXPOSE 3000 ENTRYPOINT exec java 
$JAVA_OPTS -jar lyceoaiproject.jar # For Spring-Boot 
project, use the entrypoint below to reduce Tomcat 
startup time. #ENTRYPOINT exec java $JAVA_OPTS 
-Djava.security.egd=file:/dev/./urandom -jar 
lyceoaiproject.jar

{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Launch Chrome against localhost",
            "url": "http://localhost:5000",
            "webRoot": "${workspaceFolder}"
        }
    ]
}
