# RustPoker

[![Build Status](https://travis-ci.org/kmurf1999/rust_poker.svg?branch=master)](https://travis-ci.org/kmurf1999/rust_poker)
[![docs.rs](https://docs.rs/rust_poker/badge.svg)](https://docs.rs/rust_poker)
[![crates.io](https://img.shields.io/crates/v/rust_poker.svg)](https://crates.io/crates/rust_poker)

A poker library written in rust.

 - Multithreaded range vs range equity calculation
 - Fast hand evaluation
 - Efficient hand indexing


## Installation

Add this to your `Cargo.toml`:
```
[dependencies]
rust_poker = "0.1.13"
```
**Note**: The first build of an application using `rust_poker` will take extra time to generate the hand evaluation table

## Developing Bindings

Use virtual env `virtualenv .venv`.

Enable the envirnmoent `source .venv/bin/activate`

Run `maturin develop` to create ptyhon lib with bindings, it will automatically put it inside the python packages dir.

To test out point the ipynb notebooks kernel to virtualenv and then just run the package.

To install pytohn packages `pip install poetry && poetry install --no-root`

## Hand Evaluator

Evaluates the strength of any poker hand using up to 7 cards.

### Usage

```rust
use rust_poker::hand_evaluator::{Hand, CARDS, evaluate};
// cards are indexed 0->51 where index is 4 * rank + suit
let hand = Hand::empty() + CARDS[0] + CARDS[1];
let score = evaluate(&hand);
println!("score: {}", score);
```

## Equity Calculator

Calculates the range vs range equities for up to 6 different ranges specified by equilab-like range strings.
Supports monte-carlo simulations and exact equity calculations

### Usage

```rust
use rust_poker::hand_range::{HandRange, get_card_mask};
use rust_poker::equity_calculator::approx_equity;
let ranges = HandRange::from_strings(["AK,22+".to_string(), "random".to_string()].to_vec());
let public_cards = get_card_mask("2h3d4c".to_string());
let stdev_target = 0.01;
let n_threads = 4;
let equities = approx_equity(&ranges, public_cards, n_threads, stdev_target);
println!("player 1 equity: {}", equities[0]);
```

## Credit

The hand evaluator and equity calculator library is a rust rewrite of **zekyll's** C++ equity calculator, [OMPEval](https://github.com/zekyll/OMPEval)

## License

This project is MIT Licensed

Copyright (c) 2020 Kyle Murphy
