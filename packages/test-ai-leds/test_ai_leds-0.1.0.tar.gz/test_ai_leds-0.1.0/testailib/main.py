from .crew_xUnit import xunit_generation, info_gatherer_crew
from .crew_gherkin import generate_gherkin
import argparse
import os
from dotenv import load_dotenv

def main() -> str:
    parser = argparse.ArgumentParser(description="Processa os parâmetros")
    parser.add_argument("generate", type=str, help="O que você deseja gerar (gherkin ou xunit)")
    parser.add_argument("--andes", type=str, help="Casos de usuário para gerar o Gherkin")
    parser.add_argument("--user_case", type=str, help="Casos de usuário para gerar o Gherkin")
    parser.add_argument("--feature", type=str, help="A feature para gerar o código xUnit")
    parser.add_argument("--dto_source", type=str, help="O caminho para os arquivos DTO")
    parser.add_argument("--swagger_path", type=str, help="O caminho para o documento Swagger")
    args = parser.parse_args()

    if args.generate == 'gherkin':
        if not args.user_case:
            parser.error("--user_case deve ser fornecido quando --generate é 'gherkin'")
        generate_gherkin(args.user_case)

    if args.generate == "xunit":
        if not args.feature:
            parser.error("--feature deve ser fornecida quando --generate é 'xunit'")

        # if not args.dto_source:
        #     parser.error("--dto_source deve ser fornecida quando --generate é 'xunit'")

        # if not args.swagger_path:
        #     parser.error("--swagger_path deve ser fornecida quando --generate é 'xunit'")

        swagger_path = os.getenv("SWAGGER_PATH")
        dto_source = os.getenv("DTO_SOURCE")
        xunit_generation(args.feature, swagger_path, dto_source)
    

if __name__ == "__main__":
    main()