from typing import Tuple
from typing import Optional

from thumbny.base import CommandBase
from thumbny.models import TemplateModel
from thumbny.models import LabelModel
from thumbny.models import FillerModel
from thumbny.enums import PositionTypeEnum
from thumbny.enums import XPositionEnum
from thumbny.enums import YPositionEnum


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class GenerateCommand(CommandBase):
    def __init__(self, model: FillerModel) -> None:
        super().__init__()
        self.model = model

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def _get_filename(self) -> str:
        return self.model.name.replace(" ", "_")

    def _get_template(self) -> TemplateModel:
        template = self.tm.get_template_info(self.model.template_key)
        return TemplateModel.make(template)

    def _find_template(self,
                       template: TemplateModel,
                       label_key: str) -> Optional[LabelModel]:
        for template_label in template.labels:
            if template_label.key == label_key:
                return template_label
        return None

    def execute(self) -> None:
        filename = self._get_filename()
        template = self._get_template()

        image = Image.new(mode="RGB",
                          size=(template.width, template.height),
                          color=template.background_color)

        draw = ImageDraw.Draw(image)

        if template.background_image:
            background = Image.open(template.background_image)
            image.paste(background, (0, 0))

        for label in self.model.labels:
            template_label = self._find_template(template, label.key)

            if template_label.font_family:
                try:
                    font = ImageFont.truetype(template_label.font_family,
                                              size=template_label.font_size)
                except OSError:
                    print(f"Font wasn't found at {template_label.font_family}")
            else:
                font = ImageFont.load_default(size=template_label.font_size)

            width = draw.textlength(label.value, font=font)
            height = template_label.font_size

            if template_label.position.key == PositionTypeEnum.RELATIVE.value:
                x_positions = {
                    XPositionEnum.LEFT.value: 0,
                    XPositionEnum.CENTER.value: (template.width - width) / 2,
                    XPositionEnum.RIGHT.value: template.width - width
                }

                y_positions = {
                    YPositionEnum.TOP.value: 0,
                    YPositionEnum.CENTER.value: (template.height - height) / 2,
                    YPositionEnum.BOTTOM.value: template.height - height
                }

                x_pos_key, y_pos_key = template_label.position.value.split(",")

                x_padding = 0
                y_padding = 0
                padding = template_label.padding
                if padding:
                    x_padding = padding.left - padding.right
                    y_padding = padding.top - padding.bottom

                x_text = x_positions.get(x_pos_key, 0) + x_padding
                y_text = y_positions.get(y_pos_key, 0) + y_padding

            draw.text(xy=(x_text, y_text),
                      text=label.value,
                      fill=template_label.font_color,
                      font=font)

        image.save(f"{filename}.png")
        image.show()

        print("The thumbnail has been created successfully")
