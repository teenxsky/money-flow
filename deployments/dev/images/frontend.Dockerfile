FROM oven/bun:1.2-alpine

# Local project path
ENV LOCAL_DEPLOYMENT_PATH='/deployments/dev'

WORKDIR /frontend

COPY $LOCAL_DEPLOYMENT_PATH/entrypoints/frontend.sh /frontend.sh
RUN chmod +x /frontend.sh
ENTRYPOINT ["/frontend.sh"]
