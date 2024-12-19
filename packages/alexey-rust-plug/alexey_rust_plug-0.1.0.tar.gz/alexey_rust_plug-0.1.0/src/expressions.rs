#![allow(clippy::unused_unit)]
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::fmt::Write;
use rand::prelude::*;
use serde::Deserialize;
// use pyo3_polars::export::polars_core::utils::arrow::array::{Array as PolarsArray, Int64Array as PolarsInt64Array};
use pyo3_polars::export::polars_core::utils::arrow::array::{Int64Array as PolarsInt64Array};
use linregress::{FormulaRegressionBuilder, RegressionDataBuilder, RegressionModel};
use std::collections::HashSet;


#[derive(Deserialize)]
struct AddSuffixKwargs {
    suffix: String,
}

#[polars_expr(output_type=String)]
fn add_suffix(inputs: &[Series], kwargs: AddSuffixKwargs) -> PolarsResult<Series> {
    let s = &inputs[0];
    let ca = s.str()?;
    let out = ca.apply_into_string_amortized(|value, output| {
        write!(output, "{}{}", value, kwargs.suffix).unwrap();
    });
    Ok(out.into_series())
}

#[polars_expr(output_type=String)]
fn my_str(s: &[Series]) -> PolarsResult<Series> {
    let a = s[0].str()?;
    let total = a.apply_values(|x| {
        (x.to_string() + "111").into()
    });

    Ok(total.into_series())
}

#[polars_expr(output_type=String)]
fn my_str2(inputs: &[Series]) -> PolarsResult<Series> {
    let ca: &StringChunked = inputs[0].str()?;
    let out: StringChunked = ca.apply_into_string_amortized(|value: &str, output: &mut String| {
        write!(output, "{} 111", &value).unwrap()
    });
    Ok(out.into_series())
}

#[polars_expr(output_type=String)]
fn pig_latinnify(inputs: &[Series]) -> PolarsResult<Series> {
    let ca: &StringChunked = inputs[0].str()?;
    let out: StringChunked = ca.apply_into_string_amortized(|value: &str, output: &mut String| {
        if let Some(first_char) = value.chars().next() {
            write!(output, "{}{}ay", &value[1..], first_char).unwrap()
        }
    });
    Ok(out.into_series())
}


// fn my_abs2(s: &[Series]) -> PolarsResult<Series> {   // быстрее, чем my_abs3 и my_abs4
//     let s3 = &s[0];
//     let ca = s3.f64()?;
//     // let out = ca.apply_values(|x| x.abs() + 5.0);
//     let out = ca.apply_values(|x| x + 0.5);
//     Ok(out.into_series())
// }

#[polars_expr(output_type=Int64)]
fn my_abs2(s: &[Series]) -> PolarsResult<Series> {   // быстрее, чем my_abs3 и my_abs4
    let s3 = &s[0];
    let ca = s3.i64()?;
    let out = ca.apply_values(|x| {
        if x > 50 {
            x * 2 + 14
        } else {
            x - 140
        }
    });
    Ok(out.into_series())
}

#[polars_expr(output_type=Float64)]
fn my_abs5(s: &[Series]) -> PolarsResult<Series> {
    let a = s[0].f64()?;
    let total: ChunkedArray<Float64Type> = a
        .iter()
        .map(|x| {
            x.and_then(|y| Some(y + 0.5))
        })
        .collect();

    Ok(total.into_series())
}

// #[polars_expr(output_type=Float64)]
// fn my_abs3(s: &[Series]) -> PolarsResult<Series> {
//     let a = s[0].f64()?;
//     let out = a + 0.5;
//     Ok(out.into_series())
// }

// #[polars_expr(output_type=Float64)]
// fn my_abs4(s: &[Series]) -> PolarsResult<Series> {
//     let a = s[0].clone();
//     let out = &a + 0.5;
//     Ok(out)
// }

#[polars_expr(output_type=Int64)]
fn my_sum_i64(s: &[Series]) -> PolarsResult<Series> {
    let a1_casted = s[0].cast(&DataType::Int64)?;
    let a1_c = a1_casted.i64()?;
    let a2 = s[1].i64()?;
    let out: ChunkedArray<Int64Type> = a1_c + a2;
    Ok(out.into_series())
}  

#[polars_expr(output_type=Int64)]
fn my_mult(s: &[Series]) -> PolarsResult<Series> {
    let a1 = s[0].i64()?;
    let a2 = s[1].i64()?;
    let mult = match a2.max() {
        Some(max) => max,
        None => 0,
    };
    let out = a1 * mult;
    Ok(out.into_series())
}

#[polars_expr(output_type=Float64)]
fn my_rand(s: &[Series]) -> PolarsResult<Series> {
    let distr = rand::distributions::Uniform::new_inclusive(0.0, 1.0);
    let ca = s[0].f64()?;
    let out = ca.apply_values(|_| {
        let mut rng = thread_rng();
        rng.sample(distr)
    });
    Ok(out.into_series())
}

#[polars_expr(output_type=Float64)]
fn my_rand2(s: &[Series]) -> PolarsResult<Series> {
    let size = s[0].len();
    let distr = rand::distributions::Uniform::new_inclusive(0.0, 1.0);
    let mut rng = thread_rng();
    let data: Vec<f64> = (0..size).map(|_| rng.sample(distr)).collect();
    let s1 = Series::new("a".into(), data);
    Ok(s1.into_series())
}

#[polars_expr(output_type=Int64)]
fn max_in_list(s: &[Series]) -> PolarsResult<Series> {
    let a = s[0].list()?;
    let out: ChunkedArray<Int64Type> = a
        .iter()
        .map(|x| x.and_then(|y| {
            let tmp = y.as_any().downcast_ref::<PolarsInt64Array>();
            tmp.and_then(|z| z.values().iter().max().copied() )
        }))
        .collect();

    Ok(out.into_series())
}

#[polars_expr(output_type=Int64)]
fn list_between3(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].list()?;
    let ca2 = s[1].i64()?;
    let ca3 = s[2].i64()?;

    let out: ChunkedArray<ListType> = ca1
        .iter()
        .zip(ca2.iter())
        .zip(ca3.iter())
        .map(|((x1, x2), x3)| {
            let t1: &Series = &Series::from_arrow("wq".into(), x1.unwrap()).unwrap();
            let t2: &ChunkedArray<Int64Type> = t1.i64().unwrap();
            let t3: ChunkedArray<Int64Type> = t2
                .iter()
                .filter(|x4| (x4 > &x2) & (x4 < &x3) )
                .collect();
            t3.into_series()
        } )
        .collect();

    Ok(out.into_series())
}

#[polars_expr(output_type=Float64)]
fn regression(s: &[Series]) -> PolarsResult<Series> {
    let mut my_set: HashSet<usize> = HashSet::new();
    let mut my_set_out: HashSet<usize> = HashSet::new();
    let mut data: Vec<(&str, Vec<f64>)> = vec![];
    let mut form: String = String::new();

    for (index, i) in s.iter().enumerate() {
        let ca: &ChunkedArray<Float64Type> = i.f64()?;
        let _out: ChunkedArray<Float64Type> = ca
            .iter()
            .enumerate()
            .map(|(x1, x2)| {
                if x2 == None {
                    my_set.insert(x1);
                    if index != 0 {
                        my_set_out.insert(x1);
                    }
                }
                x2
            })
            .collect();
    }

    for i in s {
        let ca: &ChunkedArray<Float64Type> = i.f64()?;
        let out: ChunkedArray<Float64Type> = ca
            .iter()
            .enumerate()
            .filter(|(x1, _x2 )| {
                !my_set.contains(&x1)
            })
            .map(|(_x1, x2)| { x2 })
            .collect();
        
        let t = out.to_vec_null_aware().unwrap_left();  
        data.push((i.name(), t));
        form += &(i.name().to_string() + " + "); 
    }

    let formula = &form.replacen("+", "~", 1)[..(form.len() - 3)];
    let data = RegressionDataBuilder::new().build_from(data).unwrap();
    let model: RegressionModel = FormulaRegressionBuilder::new()
        .data(&data)
        .formula(formula)
        .fit().unwrap();

    fn calc(model: &RegressionModel, index: &usize, s: &[Series]) -> Option<f64> {
        let mut data: Vec<(&str, Vec<f64>)> = vec![];
        for i in &s[1..] {
            let t: f64 = i.get(*index).unwrap().try_extract().unwrap();
            data.push((i.name(), vec![t]));
        }
        let prediction: Vec<f64> = model.predict(data).unwrap();            
        Some(prediction[0])
    }
    
    let ca = s[0].f64()?;
    let out: ChunkedArray<Float64Type> = ca
        .iter()
        .enumerate()
        .map(|(x1, _x2)| {
            if !my_set_out.contains(&x1) {
                calc(&model, &x1, &s)
            } else {
                None
            }
        })
        .collect();

    Ok(out.into_series())     
}


#[polars_expr(output_type=Int64)]
fn add(s: &[Series]) -> PolarsResult<Series> {
    let ca = s[0].i64()?;
    let out: ChunkedArray<Int64Type> = ca
        .iter()
        .map(|x1| x1.and_then(|x2| {
            if x2 > 50 {
                Some(x2 * 2 + 14)
            } else {
                Some(x2 - 140)
            }
        }))
        .collect();

    Ok(out.into_series())   
}

#[polars_expr(output_type=String)]
fn str_from_col(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].str()?;
    let ca2 = &s[1].str()?.unique().unwrap();

    let out: ChunkedArray<StringType> = ca1
        .iter()
        .map(|x1| x1.and_then(|x2| {

            let r: HashSet<&str> = x2
                .split_whitespace()
                .collect();

            let r2 = &ca2.iter()
                .filter(|x3| match x3 {
                    Some(v) => r.contains(v),
                    None => false,
                })
                .next();

            r2.unwrap_or_else(|| None)

        }))
        .collect();


    Ok(out.into_series())
}

use regex::Regex;

#[polars_expr(output_type=String)]
fn str_from_col2(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].str()?;
    let ca2 = s[1].str()?;
    let ca3 = ca2.unique().unwrap();
    let re = Regex::new(r"[ ]").unwrap();

    let out: ChunkedArray<StringType> = ca1
        .iter()
        .zip(ca2.iter())
        .map(|(x1, x5)| {
            match x5 {
                Some(_v1) => None,
                None => {
                    x1.and_then(|x2| {
                        let r: HashSet<String> = re
                            .split(x2)
                            // .split_whitespace()
                            // .split(|d| d == ' ')
                            .map(|x4| x4.to_ascii_lowercase() )
                            .collect();
        
                        let r2: &Option<Option<&str>> = &ca3.iter()
                            .find(|x3: &Option<&str>| match x3 {
                                Some(v) => r.contains(&v.to_string()),
                                None => false,
                            });
        
                        r2.unwrap_or_else(|| None)
                    })
                }
            }
        })
        .collect();


    Ok(out.into_series())
}

#[polars_expr(output_type=String)]
fn str_from_col3(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].str()?;
    let ca2 = s[1].str()?;
    let hs: HashSet<&str> = ca2
        .iter()
        .filter_map(|opt| opt)
        .collect();
    let re = Regex::new(r"[ ]").unwrap();

    let out: ChunkedArray<StringType> = ca1
        .iter()
        .zip(ca2.iter())
        .map(|(x1, x5)| {
            match x5 {
                Some(_v1) => None,
                None => {
                    x1.and_then(|x2| {
                        re.split(x2)
                        .find_map(|x3|  {
                            let t1 = x3.to_lowercase();

                            match hs.contains(&t1.as_str()) {
                                true => Some(t1),
                                false => None,
                            }
                        })
                    })
                }
            }
        })
        .collect();

    Ok(out.into_series())
}


#[polars_expr(output_type=Int64)]
fn max_date(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?.max().clone().unwrap();

    Ok(Series::new("a2".into(), &[ca1]))
}


#[polars_expr(output_type=Int64)]
fn my_sum(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?;

    let out = ca1
        .iter()
        .fold(0, |x1, x2| x1 + x2.unwrap());

    Ok(Series::new("a2".into(), &[out]))
}

#[polars_expr(output_type=Int64)]
fn my_sum2(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?;

    let out: ChunkedArray<Int64Type> = ca1
        .iter()
        .scan(0, |x1: &mut i64, x2| {
            *x1 += x2.unwrap();
            Some(Some(*x1))
        })
        .collect();

    Ok(out.into_series())
}

use std::sync::Arc;
use std::thread;

// #[polars_expr(output_type=Int64)]
// fn my_sum3(s: &[Series]) -> PolarsResult<Series> {

//     let ss1 = s[0].slice(0, 51000/4);
//     let ss2 = s[0].slice(51000/4, 51000/4);
//     let ss3 = s[0].slice(51000/2, 51000/4);
//     let ss4 = s[0].slice((51000*3)/4, 51000/4);

//     println!("s1 {}", ss1.len());
//     println!("s2 {}", ss2.len());
//     println!("s3 {}", ss3.len());
//     println!("s4 {}", ss4.len());


//     let t1 = thread::spawn(move || {
//         let ca = ss1.i64().unwrap();
//         let out = ca
//             .iter()
//             .fold(0, |x1, x2| x1 + x2.unwrap());

//         out
//     });

//     let t2 = thread::spawn(move || {
//         let ca = ss2.i64().unwrap();
//         let out = ca
//             .iter()
//             .fold(0, |x1, x2| x1 + x2.unwrap());

//         out
//     });

//     let t3 = thread::spawn(move || {
//         let ca = ss3.i64().unwrap();
//         let out = ca
//             .iter()
//             .fold(0, |x1, x2| x1 + x2.unwrap());

//         out
//     });

//     let t4 = thread::spawn(move || {
//         let ca = ss4.i64().unwrap();
//         let out = ca
//             .iter()
//             .fold(0, |x1, x2| x1 + x2.unwrap());

//         out
//     });



//     let r1 = t1.join().unwrap();
//     println!("r1 {}", r1);
//     let r2 = t2.join().unwrap();
//     println!("r2 {}", r2);
//     let r3 = t3.join().unwrap();
//     println!("r3 {}", r3);
//     let r4 = t4.join().unwrap();
//     println!("r4 {}", r4);

//     Ok(Series::new("a2".into(), &[r1 + r2 + r3 + r4]))
// }

// 1382375998


#[polars_expr(output_type=Int64)]
fn my_sum3(s: &[Series]) -> PolarsResult<Series> {
    let ser = Arc::new(s[0].clone());

    let ss1 = Arc::clone(&ser);
    let ss2 = Arc::clone(&ser);
    let ss3 = Arc::clone(&ser);
    let ss4 = Arc::clone(&ser);
    // let l = ser.len();
    let l = Arc::new(ser.len());
    let ll1 = Arc::clone(&l);
    let ll2 = Arc::clone(&l);
    let ll3 = Arc::clone(&l);
    let ll4 = Arc::clone(&l);


    // println!("l {} ", ser.len());

    let t1 = thread::spawn(move || {
        let ca = ss1.i64().unwrap();
        let ca2 = &ca.slice(0, *ll1/4);
        // print!("len t1 {}", ca2.len());
        let out = ca2
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let t2 = thread::spawn(move || {
        let ca = ss2.i64().unwrap();
        let ca2 = &ca.slice((*ll2/4).try_into().unwrap(), *ll2/4);
        // print!("len t2 {}", ca2.len());
        let out = ca2
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let t3 = thread::spawn(move || {
        let ca = ss3.i64().unwrap();
        let ca2 = &ca.slice((*ll3/2).try_into().unwrap(), *ll3/4);
        // print!("len t3 {}", ca2.len());
        let out = ca2
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let t4 = thread::spawn(move || {
        let ca = ss4.i64().unwrap();
        let ca2 = &ca.slice((*ll4*3/4).try_into().unwrap(), *ll4/4+400000);
        // print!("len t4 {}", ca2.len());
        let out = ca2
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });



    let r1 = t1.join().unwrap();
    // println!("r1 {}", r1);
    let r2 = t2.join().unwrap();
    // println!("r2 {}", r2);
    let r3 = t3.join().unwrap();
    // println!("r3 {}", r3);
    let r4 = t4.join().unwrap();
    // println!("r4 {}", r4);

    Ok(Series::new("a2".into(), &[r1 + r2 + r3 + r4]))
}


#[polars_expr(output_type=Int64)]
fn my_sum4(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?;
    let mut t: i64 = 0;

    let _out: ChunkedArray<Int64Type> = ca1
        .iter()
        .map(|x1| {
            t += x1.unwrap();
            x1
        })
        .collect();

    // dbg!(&t);
    Ok(Series::new("a2".into(), &[t]))
}

#[polars_expr(output_type=Int64)]
fn my_sum5(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?;
    let mut t: i64 = 0;

    let _out = ca1
        .iter()
        .for_each(|x1| {
            t += x1.expect("None!!");
        });

    Ok(Series::new("a2".into(), &[t]))
}

#[polars_expr(output_type=Int64)]
fn my_sum6(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?;
    let ca2 = s[1].i64()?;
    let ca3 = s[2].i64()?;
    let ca4 = s[3].i64()?;

    let out = ca1
        .iter()
        .zip(ca2.iter())
        .zip(ca3.iter())
        .zip(ca4.iter())
        .fold(0, |x1, (((x2, x3), x4), x5)| x1 + x2.unwrap() + x3.unwrap() + x4.unwrap() + x5.unwrap());

    Ok(Series::new("a2".into(), &[out]))
}

#[polars_expr(output_type=Int64)]
fn my_sum7(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?.clone();
    let ca2 = s[1].i64()?.clone();
    let ca3 = s[2].i64()?.clone();
    let ca4 = s[3].i64()?.clone();

    let t1 = thread::spawn(move || {
        let out = ca1
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let t2 = thread::spawn(move || {
        let out = ca2
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let t3 = thread::spawn(move || {
        let out = ca3
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let t4 = thread::spawn(move || {
        let out = ca4
            .iter()
            .fold(0, |x1, x2| x1 + x2.unwrap());

        out
    });

    let r1 = t1.join().unwrap();
    let r2 = t2.join().unwrap();
    let r3 = t3.join().unwrap();
    let r4 = t4.join().unwrap();

    Ok(Series::new("a2".into(), &[r1 + r2 + r3 + r4]))
}

#[polars_expr(output_type=Int64)]
fn my_sum8(s: &[Series]) -> PolarsResult<Series> {
    let ca1 = s[0].i64()?;
    let ca2 = s[1].i64()?;
    let ca3 = s[2].i64()?;
    let ca4 = s[3].i64()?;
    print!("len t1 {}", ca1.len());
    print!("len t2 {}", ca2.len());
    print!("len t3 {}", ca3.len());
    print!("len t4 {}", ca4.len());
    let mut t: i64 = 0;

    let _out = ca1
        .iter()
        .zip(ca2.iter())
        .zip(ca3.iter())
        .zip(ca4.iter())
        // .fold(0, |x1, (((x2, x3), x4), x5)| x1 + x2.unwrap() + x3.unwrap() + x4.unwrap() + x5.unwrap());
        .for_each(|(((x2, x3), x4), x5)| {
            t += x2.unwrap() + x3.unwrap() + x4.unwrap() + x5.unwrap();
    });

    Ok(Series::new("a2".into(), &[t]))
}

