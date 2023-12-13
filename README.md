# Cloud_TP3
Para cada task, os comandos devem ser executados dentro de suas respectivas pastas.
### TASK 1
Deletando pod e arquivos no namespace se existirem.
```
kubectl delete deploy serverless-redis
kubectl delete configmap pyfile
kubectl delete configmap outputkey
```
Criando files `pyfile.yaml`, `outputkey.yaml` e seus respectivos configmap, e criando pod.
```
kubectl create configmap pyfile --from-file pyfile=function.py --output yaml > configmaps/pyfile.yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=leonardooliveira-proj3-output --output yaml > configmaps/outputkey.yaml
kubectl -n leonardomaia apply -f deployment.yaml
```
Para ver se esta correto, verifique se chegou informacao.
```
redis-cli
GET leonardooliveira-proj3-output
```
### TASK 2
Usamos `git actions` para atualizar a imagem do dockerhub.

Para esta task sera preciso o pod da task1 
ou pod da taks3 rodando para o dashboard retirar informacoes.

Subindo servico
```
kubectl -n leonardomaia apply -f service.yaml
```
Criando ou Renovando pod
```
kubectl delete deploy dashboard
kubectl -n leonardomaia apply -f deployment.yaml
```
Deve-se colocar forward para acessar o servico em Ports do VSCode.
```
<ip Cluster>:32196
```
### TASK 3
Usamos `git actions` para atualizar a imagem do dockerhub.

Deletando pod e arquivos no namespace se existirem.
```
kubectl delete deploy runtime
kubectl delete configmap pyfile
kubectl delete configmap outputkey
```
Criando apenas configmap e criando pod.
```
kubectl create configmap pyfile --from-file pyfile=../task1/function.py --output yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=leonardooliveira-proj3-output --output yaml
kubectl -n leonardomaia apply -f deployment.yaml
```
Para ver se esta correto, verifique se chegou informacao.
```
redis-cli
GET leonardooliveira-proj3-output
```