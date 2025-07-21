---
layout: default
title: "Prolog Programming Exercises"
---

# Prolog Programming Exercises

## Exercise 1: Basic Facts and Rules

### Family Relationships

```prolog
% Facts about family relationships
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

% Rule: X is a grandparent of Z if X is parent of Y and Y is parent of Z
grandparent(X,Z) :- parent(X,Y), parent(Y,Z).

% Rule: X and Y are siblings if they have the same parent
sibling(X,Y) :- parent(Z,X), parent(Z,Y), X \= Y.
```

### Sample Queries

```prolog
?- parent(tom, bob).
% true.

?- parent(bob, X).
% X = ann ;
% X = pat.

?- grandparent(tom, ann).
% true.

?- grandparent(tom, X).
% X = ann ;
% X = pat.
```

## Exercise 2: List Operations

### Basic List Predicates

```prolog
% Check if X is a member of list L
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% Append two lists
append([], L, L).
append([H|T], L, [H|R]) :- append(T, L, R).

% Find length of a list
length([], 0).
length([_|T], N) :- length(T, N1), N is N1 + 1.
```

### Sample Queries

```prolog
?- member(3, [1,2,3,4]).
% true.

?- append([1,2], [3,4], X).
% X = [1, 2, 3, 4].

?- length([a,b,c], X).
% X = 3.
```

## Exercise 3: Knowledge Representation Example

### Animal Classification

```prolog
% Facts about animals
animal(dog).
animal(cat).
animal(robin).
animal(penguin).

% Facts about mammals
mammal(dog).
mammal(cat).

% Facts about birds
bird(robin).
bird(penguin).

% Facts about flying ability
can_fly(robin).

% Rules
warm_blooded(X) :- mammal(X).
warm_blooded(X) :- bird(X).

vertebrate(X) :- mammal(X).
vertebrate(X) :- bird(X).

% Complex rule
can_move_fast(X) :- mammal(X), can_run(X).
can_move_fast(X) :- bird(X), can_fly(X).
```

## Key Insights from Exercises

1. **Facts** are simple statements that are always true
2. **Rules** use `:-` to define logical implications 
3. **Queries** ask questions and Prolog finds all possible answers
4. **Unification** matches variables with values automatically
5. **Backtracking** finds multiple solutions by exploring alternatives

## Running the Code

These examples can be run in SWI-Prolog:
1. Save code in a `.pl` file
2. Load with `?- [filename].`
3. Run queries at the `?-` prompt

---

[← Back to Unit 4](/krr/#unit-4) | [KRR Module Home](/krr/)