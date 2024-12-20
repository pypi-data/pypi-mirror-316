use pyo3::prelude::*;

#[pymodule]
mod tictoc {
    use super::*;
    use std::time::Instant;
    use pyo3::exceptions::PyException;
    
    #[pyclass(name = "results")]
    #[derive(Clone, Debug, PartialEq)]
    struct Results {
        #[pyo3(get)]
        nanos: u128,
        #[pyo3(get)]
        micros: u128,
        #[pyo3(get)]
        millis: u128,
        #[pyo3(get)]
        seconds: f64,
    }
    
    #[derive(Clone)]
    #[pyclass(name = "init")]
    pub struct Init {
        time: Instant,
        #[pyo3(get)]
        results: Results,
        status: bool,
    }
    
    #[pymethods]
    impl Init {
        #[new]
        fn new() -> Self {
            let res = Results {
                nanos: 0,
                micros: 0,
                millis: 0,
                seconds: 0.0,
            };
            Init {
                time: Instant::now(),
                results: res,
                status: false,
            }
        }
    
        fn tic(&mut self) -> PyResult<Init> {
            self.time = Instant::now();
            self.status = true;
            Ok(Init::new())
        }
    
        #[pyo3(signature = (tic=None))]
        fn toc(&mut self, tic: Option<Init>) -> PyResult<Results> {
            let elapsed_time = match tic {
                Some(ref tic) => tic.time.elapsed(),
                None => self.time.elapsed(),
            };
            let status = match tic {
                Some(ref _tic) => true,
                None => self.status,
            };
            if status == false {
                Err(PyException::new_err("tic() must be called before toc()"))    
            } else {       
                self.results = Results {
                    nanos: elapsed_time.as_nanos(),
                    micros: elapsed_time.as_micros(),
                    millis: elapsed_time.as_millis(),
                    seconds: elapsed_time.as_secs_f64(),
                };
                println!("The elapsed time was {} seconds.",self.results.seconds);
                Ok(self.results.clone())
            }
        }
    }

    #[test]
    fn test_new() {
        let init = Init::new();
        assert_eq!(init.results.nanos,0);
    }
    
    #[test]
    fn test_tic() {
        let mut init = Init::new();
        let time1 = init.time;
        let _ = init.tic();
        let time2 = init.time;
        assert!(time2 > time1)
    }

    #[test]
    fn test_toc() {
        let mut init = Init::new();
        let _ = init.tic();
        println!("{}","test");
        let _ = init.toc(None).unwrap();
        assert!(init.results.nanos > 0);
    }

    #[test]
    fn test_passing_tic_to_toc() {
        let mut init = Init::new();
        let tic_obj = init.tic().unwrap();
        println!("{}","test");
        let results = init.toc(Some(tic_obj)).unwrap();
        assert!(init.results.nanos > 0);
        assert_eq!(init.results,results)
    }

    #[test]
    fn test_multiple_calls() {
        let mut init = Init::new();
        let first_tic = init.tic().unwrap();
        println!("{}","test");
        let second_tic = init.tic().unwrap();
        println!("{}","test");
        let results2 = init.toc(Some(second_tic)).unwrap();
        let results = init.toc(Some(first_tic)).unwrap();
        assert!(results.nanos > results2.nanos);
    }

    #[test]
    fn test_toc_before_tic() {
        let mut init = Init::new();
        //assert!(init.toc(None).is_err())
        pyo3::prepare_freethreaded_python();
        let e = init.toc(None).unwrap_err();
        assert_eq!(e.to_string(),"Exception: tic() must be called before toc()")
    }
}
