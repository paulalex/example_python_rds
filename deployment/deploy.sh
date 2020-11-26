#!/usr/bin/env bash
set -e

CDIR=$(cd `dirname "$0"` && pwd)
cd "$CDIR"

print_red() {
  printf '%b' "\033[91m$1\033[0m\n"
}

print_green() {
  printf '%b' "\033[92m$1\033[0m\n"
}

find_and_replace_templates() {
    print_green "[INFO] Finding and replacing in base templates"
    # Replace on base kustomization config
    sed "s/IMAGE_TAG/${SUPPLIED_IMAGE_TAG}/g" base/template/kustomization.yaml > base/kustomization.yaml
    sed "s/NAMESPACE_PLACEHOLDER/${NAMESPACE}/g" base/template/namespace.yaml > base/namespace.yaml
    sed "s/NAMESPACE_PLACEHOLDER/${NAMESPACE}/g" base/template/ingress.yaml > base/ingress.yaml
    sed "s/NAMESPACE_PLACEHOLDER/${NAMESPACE}/g" base/template/iam-service-account.yaml > base/iam-service-account.yaml

    # Replace in generated files
    print_green "[INFO] Finding and replacing in generated files"
    sed "s/NAMESPACE_PLACEHOLDER/${NAMESPACE}/g" ${FOLDER}template/kustomization.yaml |
    sed "s/DB_URL_PLACEHOLDER/${DATABASE_URL}/g" |
    sed "s/DB_ENGINE_PLACEHOLDER/${DATABASE_ENGINE}/g" |
    sed "s/DB_PORT_PLACEHOLDER/${DATABASE_PORT}/g" |
    sed "s/DB_NAME_PLACEHOLDER/${DATABASE_NAME}/g" |
    sed "s/DB_USER_PLACEHOLDER/${DATABASE_USER}/g" |
    sed "s/DB_PWD_PLACEHOLDER/${DATABASE_PASSWORD}/g" > ${FOLDER}kustomization.yaml
}

clean_up_environment() {
  print_green '[INFO] Cleaning up generated files'
  eval "rm base/kustomization.yaml"
  eval "rm base/namespace.yaml"
  eval "rm base/ingress.yaml"
  eval "rm base/iam-service-account.yaml"
  eval "rm ${FOLDER}kustomization.yaml"
}

build() {
    print_green "[INFO] Deploying Application"
    eval "kubectl kustomize ${FOLDER} | kubectl apply -f -"
}

debug() {
    print_green "[DEBUG] Deploying ddc-example-rds-python into namespace ${NAMESPACE} using folder ${FOLDER}"
    find_and_replace_templates
    eval "kubectl kustomize ${FOLDER}"
    clean_up_environment
}

info() {
    print_green "[INFO] Namespaces"
    KUBECTL="kubectl ${KUBECTL_PARAMS} --namespace=${NAMESPACE}"
    eval "${KUBECTL} get namespaces --show-labels"
    print_green "[INFO] Pods"
    eval "${KUBECTL} get pods --show-labels"
    print_green "[INFO] Services"
    eval "${KUBECTL} get services --show-labels"
    print_green "[INFO] Network Policies"
    eval "${KUBECTL} get networkpolicies --show-labels"
    print_green "[INFO] Configmaps"
    eval "${KUBECTL} get configmaps --show-labels"
    print_green "[INFO] Ingress"
    eval "${KUBECTL} get ingress --show-labels"
    print_green "[INFO] Service Accounts"
    eval "${KUBECTL} get sa --show-labels"
    print_green "[INFO] Deployment Complete"
}

deploy() {
    print_green "[INFO] Deploying ddc-example-rds-python into namespace ${NAMESPACE} using folder ${FOLDER}"
    find_and_replace_templates
    build
    clean_up_environment
    info
}

OVERLAY=${1?You must pass in the name of the environment to deploy example-rds-python into [dev, test, non-prod, prod]}
BRANCH_ID=${2?You must specify the branch name you want to deploy}
SUPPLIED_IMAGE_TAG=${3?You must specify the tag of the image you want to deploy}
DATABASE_URL=${4?You must specify the database endpoint}
DATABASE_ENGINE=${5?You must specify the database engine}
DATABASE_PORT=${6?You must specify the database port}
DATABASE_NAME=${7?You must specify the database name}
DATABASE_USER=${8?You must specify the database username}
DATABASE_PASSWORD=${9?You must specify the database password}
NAMESPACE="example-rds-python-${BRANCH_ID}"
FOLDER="overlays/${OVERLAY}/"

if [[ $3 == 'debug' ]]; then
    echo "[INFO] Running in debug mode"
    debug
else
    echo "[INFO] Supplied Arguments list $@"
    deploy
fi






