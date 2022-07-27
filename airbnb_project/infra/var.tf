variable "docdb_username" {
  default = "docdb"
}

variable "docdb_password" {
  default = "password"
}


variable "lambda_query_zip" {
  default = "../lambda_functions/query.zip"
}

variable "lambda_layers_file" {
  default = "../lambda_functions/package.zip"
}
