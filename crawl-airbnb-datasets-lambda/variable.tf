variable "role_name" {
    type = string
    description = "(optional) describe your variable"
    default="test-lambda-airbnb"
}

variable "s3_bucket" {
    type = string
    description = "(optional) describe your variable"
    default = "my-airbnb-csv"
}