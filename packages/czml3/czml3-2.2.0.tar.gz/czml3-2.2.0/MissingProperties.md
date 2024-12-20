# Missing Properties & Broken Validations

This is an incomplete list of all the properties and inputs to properties that are missing in czml3.

The following CZML properties need to be added:
- [LineOffset](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineOffset)
- [LineThickness](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineThickness)
- [LineCount](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineCount)
- [Repeat](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Repeat)
- [NodeTransformations](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NodeTransformations)
- [Articulations](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Articulations)
- [PixelOffset](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PixelOffset)
- [VelocityReferenceValue](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/VelocityReferenceValue)
- [Font](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Font)
- [BackgroundPadding](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/BackgroundPadding)
- [CartographicRectangleRadiansValue](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicRectangleRadiansValue)
- [CartographicRectangleDegreesValue](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicRectangleDegreesValue)
- [Polyline](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Polyline)
- [CustomProperties](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CustomProperties)
- [CustomProperty](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CustomProperty)
- [PolylineVolume](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineVolume)

The following CZML properties have missing inputs:
- [Packet](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet)
- [Billboard](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Billboard)
- [Label](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Label)
- [Rectangle](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Rectangle)
- [InterpolatableProperty](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/InterpolatableProperty)

Broken validations:
- The `Uri._check_uri` does not check base64 images correctly.
- The `Uri._check_uri` does not allow relative paths, which seems to be supported despite it not being a valid uri value.