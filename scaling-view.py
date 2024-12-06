  GNU nano 7.2                                                                                                                                      scaling-view.py                                                                                                                                               
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os
from random import randint
from time import sleep
from blinkt import set_pixel, show

def contar_pods(node_name: str, label_selector: str, kubeconfig_path: str = None) -> int:
    """
    Conta o número de pods que estão rodando em um nó específico e que correspondem a um label selector.

    :param node_name: Nome do nó Kubernetes.
    :param label_selector: Selector de labels para filtrar os pods.
    :param kubeconfig_path: Caminho para o arquivo kubeconfig. Se None, tenta usar configuração in-cluster.
    :return: Número de pods que correspondem aos critérios.
    """
    try:
        if kubeconfig_path:
            # Carrega a configuração a partir do arquivo kubeconfig especificado
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            # Tenta carregar a configuração in-cluster
            config.load_incluster_config()
    except Exception as e:
        print(f"Erro ao carregar a configuração do Kubernetes: {e}")
        return 0

    v1 = client.CoreV1Api()

    field_selector = f"spec.nodeName={node_name}"

    try:
        pods = v1.list_pod_for_all_namespaces(
            label_selector=label_selector,
            field_selector=field_selector,
            watch=False
        )
    except ApiException as e:
        print(f"Erro ao listar os pods: {e}")
        return 0

    return len(pods.items)

if __name__ == "__main__":
    NOME_DO_NO = "cluster-m7"
    LABEL_SELECTOR = "app=site-comp-nuvem"

    CAMINHO_KUBECONFIG = os.getenv('KUBECONFIG', None)  # Usa a variável de ambiente KUBECONFIG se definida

    while True:
        numero_de_pods = contar_pods(
            node_name=NOME_DO_NO,
            label_selector=LABEL_SELECTOR,
            kubeconfig_path=CAMINHO_KUBECONFIG
        )

        if numero_de_pods > 0:
            for pixel in range(numero_de_pods):
                # Calcula os valores de r, g, b. Assegure-se de que os valores estão dentro de 0-255
                r = int(255 * 0.125 * numero_de_pods)
                g = int(255 * 0.125 * numero_de_pods)
                b = int(255 * 0.125 * numero_de_pods)

                set_pixel(pixel, r, g, b)
                show()
                sleep(2)
        else:
            for pixel in range(8):
                set_pixel(pixel, 0, 0, 0)
                show()
                sleep(2)

