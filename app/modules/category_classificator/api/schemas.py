from marshmallow import Schema, fields


class PredictRequestSchema(Schema):
    text = fields.Str(required=True, error_messages={"required": "El campo 'text' es obligatorio."})


class TrainModelResponseSchema(Schema):
    message = fields.Str()
