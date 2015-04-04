namespace java com.winterfarmer.service.coniferous.gen

exception InvalidSystemClock {
  1: string message,
}

exception InvalidUserAgentError {
  1: string message,
}

service Coniferous {
  i64 get_worker_id()
  i64 get_timestamp()
  i64 get_ids(1:string token, 2:i16 count)
  list<i64> get_data_center_id()
}

