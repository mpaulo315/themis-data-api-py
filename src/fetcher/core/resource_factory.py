from fetcher.core.job import DatasetType, ResourceKind, Job
from fetcher.core.resource import Resource, CamaraJSONZIPResource, CamaraJSONResource
from typings.deputado import Deputado
from typings.legislatura import Legislatura
from typings.despesa_deputado import DespesaDeputado


class ResourceFactory:
    @staticmethod
    def create(job: Job) -> Resource:
        match job.dataset_type:
            case DatasetType.DEPUTADO:
                model = Deputado
            case DatasetType.LEGISLATURA:
                model = Legislatura
            case DatasetType.DESPESA_DEPUTADO:
                model = DespesaDeputado
            case _:
                raise ValueError(f"Tipo de dataset desconhecido: {job.dataset_type}")

        match job.resource_kind:
            case ResourceKind.JSON_ZIP:
                if job.args.get("json_filename") is None:
                    raise ValueError(
                        "json_filename is required for JSON_ZIP resource kind"
                    )
                if job.args.get("url") is None:
                    raise ValueError("url is required for JSON_ZIP resource kind")
                return CamaraJSONZIPResource(
                    model=model,
                    url=job.args.get("url"),
                    json_filename=job.args.get("json_filename"),
                )
            case ResourceKind.JSON:
                if job.args.get("url") is None:
                    raise ValueError("url is required for JSON resource kind")
                return CamaraJSONResource(
                    model=model,
                    url=job.args.get("url"),
                )
            case _:
                raise ValueError(f"Tipo de recurso desconhecido: {job.resource_kind}")
