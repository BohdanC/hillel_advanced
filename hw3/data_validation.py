from marshmallow import validate
from webargs import fields

student_args = {
    "count": fields.Int(
        missing=30,
        validate=[validate.Range(min=1, max=1000)]
    )

}

bitcoin_rate_args = {
    "currency": fields.Str(
        missing='USD',
        validate=[validate.Length(min=3, max=4)],
    )
}