import argparse

from app.config import init_config, get_config
from app.config.log_config import logger
from app.models.image_meta import ImageMeta
from app.models.quote_generator_client import OpenAiClient
from app.services.asset_manager_service import AssetManagerService
from app.services.prompt_builder_service import PromptBuilderService
from app.services.quote_generator_service import QuoteGeneratorService
from app.services.image_generator_service import ImageGeneratorService


def parse_args():
    """
    Parse the command line arguments.
    """
    # Parse the arguments
    parser = argparse.ArgumentParser(
        description='''
            This script generates images with quotes using OpenAI's GPT API.
            '''
    )
    parser.add_argument(
        '--image_num',
        type=int,
        help='The number of images to generate. Default is 1.',
        required=False,
        default=1
    )

    return parser.parse_args()


def main(image_num: int = 1):
    logger.info("Generating %s images with quotes...", image_num)

    # Initialize services
    asset_manager_service = AssetManagerService
    prompt_builder_service = PromptBuilderService()
    quote_generator_service = QuoteGeneratorService(
        client=OpenAiClient(
            api_key=get_config().OPENAI_API_KEY,
            model=get_config().OPENAI_MODEL
        )
    )
    image_generator = ImageGeneratorService()

    for _ in range(image_num):
        # Create meta information holder for the image
        image_meta = ImageMeta(
            llm_model=quote_generator_service.client.model,
            prompt_version=prompt_builder_service.prompt_version
        )

        # Generate quote and caption with an LLM
        prompt, prompt_extras = prompt_builder_service.get_prompt_variation()
        quote, caption = quote_generator_service.get_quote_and_caption(prompt)

        # Generate image with the quote
        image_generator.set_random_color_and_font_scheme()
        generated_image = image_generator.create_image_with_quote(quote)

        # Update the metadata
        image_meta.update(
            quote=quote,
            caption=caption,
            prompt_extras=prompt_extras,
            img_meta=image_generator.get_meta()
        )

        # Save the image and its metadata
        asset_manager_service.save_image_meta(image_meta)
        asset_manager_service.save_image(generated_image, image_meta.id)
        logger.info("Asset with id '%s' generated successfully.", image_meta.id)


if __name__ == '__main__':
    # Retrieve the application arguments
    args = parse_args()
    # Initialize the project configuration
    init_config(env='prod')

    main(args.image_num)
