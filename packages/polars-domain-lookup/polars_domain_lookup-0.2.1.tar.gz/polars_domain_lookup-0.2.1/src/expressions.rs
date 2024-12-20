#![allow(clippy::unused_unit)]
use serde::Deserialize;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::{collections::HashMap, fs::read_to_string};

#[derive(Deserialize)]
struct TopDomainsFileKwargs {
    top_domains_file: String,
}

#[polars_expr(output_type=Boolean)]
fn is_common_domain(inputs: &[Series], kwargs: TopDomainsFileKwargs) -> PolarsResult<Series> {
    // let cisco_umbrella: Vec<String> = get_common_domains(&kwargs.top_domains_file);
    let top_domains: HashMap<String, ()> = get_common_domains_hashmap(&kwargs.top_domains_file);

    let ca: &StringChunked = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(
        DataType::Boolean, |x| top_domains.contains_key(&x.to_string())
    );
    Ok(out.into_series())
}

fn get_common_domains_hashmap(filename: &str) -> HashMap<String, ()> {
    let mut map: HashMap<String, ()> = HashMap::new();

    for line in read_to_string(filename).unwrap().lines() {
        let line_string = line.to_string();

        map.insert(line_string, ());
    }

    map
}

// fn get_common_domains(filename: &str) -> Vec<String> {
//     let mut result = Vec::new();
// 
//     for line in read_to_string(filename).unwrap().lines() {
//         let line_string = line.to_string();
// 
//         result.push(line_string);
//     }
// 
//     result
// }
