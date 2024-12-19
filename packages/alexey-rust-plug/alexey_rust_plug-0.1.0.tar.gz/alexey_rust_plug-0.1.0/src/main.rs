
// use arity::broadcast_binary_elementwise;

// use pyo3_polars::export::polars_core::utils::CustomIterTools;
// use polars::series::amortized_iter::AmortSeries;

// use polars::{prelude::*, series::amortized_iter::AmortSeries};
// use pyo3_polars::export::polars_core::utils::{arrow::array::{Array, Int64Array}, rayon::iter::ParallelBridge, CustomIterTools};
// use arrow::{array::ArrowPrimitiveType, compute::kernels::aggregate::max};

// use arrow::array::{Array as ArArray, Int64Array as ArInt64Array, PrimitiveArray as ArPrimitiveArray};
use polars::{chunked_array::collect, frame::explode, prelude::*};
use pyo3::iter;
use pyo3_polars::export::polars_core::utils::{arrow::{array::{Array as PolarsArray, Int64Array as PolarsInt64Array}, buffer::Buffer}, CustomIterTools};
// use pyo3_polars::export::polars_core::utils::rayon::iter::IntoParallelRefIterator;
// use pyo3_polars::export::polars_core::utils::Container;

use std::any::type_name;

// use arrow::array::{Array, ArrayData, Int64Array};

use std::sync::Arc;
use std::thread;
// use rand::prelude::*;
// use polars::df;
// use serde_json::{Result, Value};
// use std::borrow::Cow;
// use std::fmt::Write;
use std::collections::HashSet;

// use serde::{Deserialize, Serialize};
// use serde_json::{Result, Value};

use linregress::{FormulaRegressionBuilder, RegressionDataBuilder, RegressionModel};

use regex::Regex;


fn main() {

    fn print_type<T>(_: &T) {
        println!("{}", type_name::<T>());
    }
    // print_type(&"dssd");


    let s1 = Series::new("a1".into(), &[Some(1i64), Some(8), None, Some(16), Some(4), Some(23), Some(11), Some(13)]);
    let s2 = Series::new("a2".into(), &[Some(0i64), Some(8), Some(3), Some(16), Some(4), Some(23), Some(11), Some(13)]);
    let s3 = Series::new("a3".into(), &[Some(0i64), Some(8), Some(3), Some(16), Some(4), Some(23), Some(11), Some(13)]);
    let s4 = Series::new("a4".into(), &[Some(0i64), Some(8), Some(3), Some(16), Some(4), Some(23), Some(11), Some(13)]);


    fn my_sum(i: i64) -> PolarsResult<Series> {

        // let ca1 = s[0].i64()?;
        // let mut t: i64 = 0;
    
        // let _out = ca1
        //     .iter()
        //     .enumerate()
        //     .for_each(|(x0,x1)| {
        //         t += x1.expect(format!("None!! {x0}").as_str());
        //     });
    
        Ok(Series::new("a2".into(), &[i * 2]))
    }

    // let a = my_sum(&[s1, s2, s3, s4]);
    let a = my_sum(32);
    dbg!(&a);



    
        

}


// let s1 = Series::new("a".into(), &[
    //     None,
    //     Some("asdf"), 
    //     Some("zxcv"), 
    //     Some("qwer"),
    //     None, 
    //     Some("zxcv"),
    //     Some("mgkgmlt"),
    //     ]);
    // let s2 = Series::new("a".into(), &[
    //     // Some("dsd ttgtg qwer tkvvv"), 
    //     None,
    //     Some("oitor trotkr ASdf"), 
    //     None,
    //     None,
    //     Some("slfsSA fireore freo Mgkgmlt fjrfn"),
    //     Some("lkfsdf qwer jjkjkj"),
    //     None,
    //     ]);


// fn str_from_col(s: &[Series]) -> PolarsResult<Series> {
//     let ca1 = s[0].str()?;
//     let ca2 = s[1].str()?;
//     let hs: HashSet<&str> = ca2
//         .iter()
//         // .filter_map(|opt| opt.and_then(|opt2| Some(opt2.to_string())))
//         .filter_map(|opt| opt)
//         .collect();
//     let re = Regex::new(r"[ ]").unwrap();

//     let out: ChunkedArray<StringType> = ca1
//         .iter()
//         .zip(ca2.iter())
//         .map(|(x1, x5)| {
//             match x5 {
//                 Some(_v1) => None,
//                 None => {
//                     x1.and_then(|x2| {
//                         re.split(x2)
//                         .find_map(|x3|  {
//                             let t1 = x3.to_lowercase();

//                             match hs.contains(&t1.as_str()) {
//                                 true => Some(t1),
//                                 false => None,
//                             }
//                         })
//                     })
//                 }
//             }
//         })
//         .collect();

//     Ok(out.into_series())
// }

// dbg!(str_from_col(&[s2, s1]));



    // let s0 = Series::new("a".into(), &[1i64, 2, 3, 4]);
    // let s1 = Series::new("b".into(), &[99i64, 1, 1]);
    // let s2 = Series::new("c".into(), &[2i64, 2, 2]);
    // let s3 = Series::new("a".into(), &[1i64, 3, 5, 7]);
    // let s4 = Series::new("b".into(), &[88i64, 22, 33]);
    // let s5 = Series::new("c".into(), &[2i64, 8, 16]);
    // let l1 = Series::new("foo".into(), &[s0, s1, s2, s3, s4, s5]);
    // let l2 = Series::new("foo2".into(), &[1i64, 50, 1, 5, 0, 1]);
    // let l3 = Series::new("foo3".into(), &[3i64, 100, 2, 10, 40, 3]);

    // let s_y = Series::new("y".into(),   &[Some(1.0f64),  None,      Some(3.),  Some(4.),  Some(5.),  Some(6.),  Some(7.),  None     , Some(9.)]);
    // let s_x1 = Series::new("x1".into(), &[Some(11.0f64), Some(12.), None,      Some(14.), Some(15.), Some(16.), Some(17.), Some(18.), Some(19.)]);
    // let s_x2 = Series::new("x2".into(), &[Some(31.0f64), Some(32.), Some(33.), Some(34.), Some(35.), Some(36.), None,      Some(38.), Some(39.)]);
    // let s_x3 = Series::new("x3".into(), &[Some(15.0f64), None,      Some(35.), Some(45.), Some(55.), Some(65.), Some(75.), Some(85.), Some(95.)]);
    // let l1 = Series::new("foo".into(), &[s_y, s_x1, s_x2, s_x3]);


// fn main() {
//     let prices = vec![100.0, 200.0, 300.0];
//     let quantities = vec![1.0, 2.0, 3.0];
//     let discounts = vec![0.9, 0.8, 0.95]; // скидки в процентах

//     let total: Vec<_> = prices
//         .iter()
//         .zip(quantities.iter())
//         .zip(discounts.iter())
//         .map(|((price, quantity), discount)| price * quantity * discount)
//         .collect();

//     println!("Total costs: {:?}", total);
// }


        // let ca4= l1.list()?;
        // for i in ca4.iter() {
        //     println!("Тип элемента: {:?}", i);
        //     unsafe {
        //         match i {
        //             Some(v) => println!("{:?} нулевой элемент: {} {:?} длина: {}", 
        //                 v, 
        //                 v.get_unchecked(0), 
        //                 v.as_any().downcast_ref::<PolarsInt64Array>(),
        //                 v.len(),
        //               ),
        //             None => println!("eeeeee")
        //         } 
        //     }
        // }


        // fn foo2(x: Option<Box<dyn PolarsArray>>) -> Option<i64> {
        //     println!("{:?}", x);  
        //     match x {
        //         Some(v) => {
        //             let tmp = v.as_any().downcast_ref::<PolarsInt64Array>();
        //             tmp.and_then(|x| x.values().iter().max().copied() )
        //             // println!("{:?}", tmp.and_then(|x| Some(x.value(0)) ));
        //             // Some(v.len() as i64)
        //         },
        //         None => None,
        //     }
        // }


    // let t1 = ca1.get(2).and_then(|x| Some(x));
    // let t1 = match ca1.get(2) {
    //     Some(v) => v,
    //     None => 0,
    // };
    // match t1 {
    //     Some(value) => println!("{}", value),
    //     None => println!("dsadasdd")
    // };
    // println!("{:?}", ca1);
    // println!("{:?}", ca2);
    // println!("{:?}", out);
    // println!("{:?}", t1);
    // Ok(())


// fn main() -> Result< (), HashMap<u8, String> > {

//     struct Person{ name: String, age:u8}
    
//     fn create_person(username: &str, userage: u8) -> Result<Person, HashMap<u8, String> >{
        
//         if userage < 110{
//             let new_person = Person{name: String::from(username), age: userage };
//             Result::Ok(new_person)
//         }
//         else { 
//             let mut people: HashMap<u8, String> = HashMap::new();
//             people.insert(4, String::from("ds"));
//             Result::Err(people)
//         }
//     }

//     fn create_person2(username: &str, userage: u8) -> Person {
        
//         if userage < 110{
//             let new_person = Person{name: String::from(username), age: userage };
//             new_person
//         }
//         else { 
//             let mut people: HashMap<u8, String> = HashMap::new();
//             people.insert(4, String::from("ds"));
//             panic!("dddd {:?}", people);
//         }
//     }


//     // let tom_result = create_person("Tom", 147).unwrap();
//     // let tom_result = create_person("Tom", 147)?;
//     let tom_result = create_person2("Tom", 147);
//     println!("Name: {}  Age: {}", tom_result.name, tom_result.age);
//     Ok(())




    // let mult = match a2.max() {
    //     Some(max) => max,
    //     None => 0,
    // };



    
//     fn check(s: Option<i32>) -> i32 {
//         let check = match s {
//             Some(state) => state,
//             None => 0,
//         };
//         check
//     }



// fn tmp1(s: &[Series]) -> PolarsResult<Series> {
//     let a = s[0].f64()?;
//     let total: ChunkedArray<Float64Type> = a
//         .iter()
//         .map(|x| {
//             x.and_then(|y| Some(y + 0.5))
//         })
//         // .zip(b.iter())
//         // .map(| (x, y) | {

//         //     x.and_then(f)

//         //     // let d = x.unwrap();
//         //     // let e = y.unwrap();
//         //     // Some(2.0 * d + e)
//         // } )
//         .collect();

//     Ok(total.into_series())
// }



// fn typed_example() -> Result<()> {
//     let data = "[[1.0, 2.0, 3.0], [1.0, null, 3.0], [1.0, 2.0, 3.0]]";
//     // let data = "[1.0, null, 3.0]";
//     let vec: Vec<Vec<Option<f64>>> = serde_json::from_str(&data)?;
//     println!("Please call at the number {:?}", vec);

//     Ok(())
// }

// typed_example();


    // fn list_between(s: &[Series]) -> PolarsResult<Series> {
    //     let s1 = &s[0];
    //     let s2 = &s[1];
    //     let s3 = &s[2];
    //     let ca = s1.list()?;
    //     let ca2 = s2.i64()?;
    //     let ca3 = s3.i64()?;

    //     let out: ChunkedArray<ListType> = ca
    //         .iter()
    //         .zip(ca2.iter())
    //         .zip(ca3.iter())
    //         .map(|((x1, x2), x3)| {
    //             let t2: &Series = &Series::from_arrow("wq".into(), x1.unwrap()).unwrap();
    //             let t3 = t2.i64().unwrap();
    //             let f1 = x2.unwrap();
    //             let f2 = x3.unwrap();
    //             let r1: ChunkedArray<BooleanType> = (&t3.gt(f1) & &t3.lt(f2));
    //             let filtered = t2.filter(&r1).unwrap();
    //             filtered
    //         })
    //         .collect();

    //         Ok(out.into_series())
    // }


        // let a = l1.list().unwrap();
    // let b: ChunkedArray<ListType> = a
    //     .iter()
    //     .map(|x1| {

    //         let t2: Series = Series::from_arrow("wq".into(), x1.unwrap()).unwrap();
    //         let t3: &ChunkedArray<Int64Type> = &t2.i64().unwrap();
    //         Some(t2)

            // x1.and_then(|x2| {
            //     let t: Series = Series::from_arrow("wq".into(), x2).unwrap();
            //     Some(t)

                // let x3 = x2.as_any().downcast_ref::<PolarsInt64Array>();
                // x3.and_then(|x4| {

                //     let x5: Series = x4.values().iter().map(|x6| x6+10 ).collect();
                //     let x10: Series = x4.values().iter().collect();
                //     let x11: ChunkedArray<BooleanType> = x4.values().iter().map(|x6| (*x6 > 10) && (*x6 < 50) ).collect();
                //     // let x11: &ChunkedArray<BooleanType> = &x10.i64().unwrap().gt(10);

                //     let r: &ChunkedArray<Int64Type> = &x10.i64().unwrap();
                //     // let r1: ChunkedArray<Int64Type> = &r.apply_in_place(|v| v+5);
                //     let r1: &ChunkedArray<BooleanType> = &r.gt(10);
                //     let r2: &ChunkedArray<BooleanType> = &r.lt(50);

                //     let filtered = x10.filter(&x11).unwrap();

                //     Some(filtered)
                    
                //     // print_type(&x5);

                // } )
            // })


    //     })
    //     .collect();
    
    // println!("{:?}", b.into_series());



    // fn tmp(w: &ChunkedArray<ListType>) -> ChunkedArray<Int64Type> {
    //     w.iter()
    //     .map(|x| x.and_then(|y| {
    //         let tmp = y.as_any().downcast_ref::<PolarsInt64Array>();
    //         tmp.and_then(|z| z.values().iter().max().copied() )
    //     }))
    //     .collect()
    // }