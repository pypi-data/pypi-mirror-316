pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}

#[pymodule]
fn my_rust_module(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(greet, m)?)?;
    Ok(())
}
