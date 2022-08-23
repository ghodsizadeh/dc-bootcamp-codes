variable "docdb_username" {
  default = "docdb"
}

variable "docdb_password" {
  default = "password"
}


variable "lambda_query_zip" {
  default = "../lambda_functions/query.zip"
}

variable "lambda_booking_zip" {
  default = "../lambda_functions/booking.zip"
}
variable "lambda_update_db_zip" {
  default = "../lambda_functions/update_db.zip"
}

variable "lambda_layers_file" {
  default = "../lambda_functions/package.zip"
}
