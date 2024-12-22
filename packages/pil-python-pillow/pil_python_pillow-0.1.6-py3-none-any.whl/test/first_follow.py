'''
Creating comprehensive **First & Follow sets**, a **Symbol Table**, and a **Parse Table** for a SQL compiler is an extensive task due to SQL's rich and complex grammar. However, I can provide a detailed example covering key aspects of SQL parsing. This example will include:

1. **Grammar Rules**: A simplified SQL grammar.
2. **First Sets**: For each non-terminal.
3. **Follow Sets**: For each non-terminal.
4. **Symbol Table**: Listing terminals and non-terminals.
5. **Parse Table**: Based on the grammar and First & Follow sets.

This foundation can be expanded to cover more SQL scenarios as needed.

---

## 1. Simplified SQL Grammar

We'll use a simplified subset of SQL focusing on `SELECT` statements. Here's the grammar in Backus-Naur Form (BNF):

```
1. <stmt> ::= <select_stmt> ;

2. <select_stmt> ::= SELECT <select_list> FROM <table_list> [WHERE <condition>] ;

3. <select_list> ::= * | <column_list> ;

4. <column_list> ::= <column> {, <column>} ;

5. <column> ::= identifier ;

6. <table_list> ::= <table> {, <table>} ;

7. <table> ::= identifier ;

8. <condition> ::= <expression> ;

9. <expression> ::= <column> <operator> <value> ;

10. <operator> ::= = | <> | < | > | <= | >= ;

11. <value> ::= number | string ;
```

**Terminals**: `SELECT`, `FROM`, `WHERE`, `*`, `,`, `=`, `<>`, `<`, `>`, `<=`, `>=`, `identifier`, `number`, `string`, `;`

**Non-Terminals**: `<stmt>`, `<select_stmt>`, `<select_list>`, `<column_list>`, `<column>`, `<table_list>`, `<table>`, `<condition>`, `<expression>`, `<operator>`, `<value>`

---

## 2. First Sets

The **First Set** for a non-terminal is the set of terminals that begin the strings derivable from the non-terminal.

| Non-Terminal    | First Set                             |
|-----------------|---------------------------------------|
| `<stmt>`        | `SELECT`                              |
| `<select_stmt>` | `SELECT`                              |
| `<select_list>` | `*`, `identifier`                     |
| `<column_list>` | `identifier`                          |
| `<column>`      | `identifier`                          |
| `<table_list>`  | `identifier`                          |
| `<table>`       | `identifier`                          |
| `<condition>`   | `identifier`                          |
| `<expression>`  | `identifier`                          |
| `<operator>`    | `=`, `<>`, `<`, `>`, `<=`, `>=`        |
| `<value>`       | `number`, `string`                    |

---

## 3. Follow Sets

The **Follow Set** for a non-terminal is the set of terminals that can appear immediately to the right of the non-terminal in some "sentential" form.

| Non-Terminal    | Follow Set                             |
|-----------------|----------------------------------------|
| `<stmt>`        | `EOF` (end of file/input)              |
| `<select_stmt>` | `;`                                     |
| `<select_list>` | `FROM`                                  |
| `<column_list>` | `,`, `FROM`                             |
| `<column>`      | `,`, `FROM`, `<operator>`               |
| `<table_list>`  | `WHERE`, `;`                            |
| `<table>`       | `,`, `WHERE`, `;`                       |
| `<condition>`   | `;`                                     |
| `<expression>`  | `;`                                     |
| `<operator>`    | `number`, `string`                      |
| `<value>`       | `;`                                     |

**Notes**:
- `EOF` denotes the end of the input.
- The Follow Sets are determined based on the grammar rules and can vary with more comprehensive grammar.

---

## 4. Symbol Table

The **Symbol Table** lists all terminals and non-terminals along with their types and any attributes.

| Symbol        | Type        | Description                                       |
|---------------|-------------|---------------------------------------------------|
| `SELECT`      | Terminal    | Keyword to start a SELECT statement               |
| `FROM`        | Terminal    | Keyword to specify table sources                  |
| `WHERE`       | Terminal    | Keyword to specify conditions                     |
| `*`           | Terminal    | Wildcard for all columns                          |
| `,`           | Terminal    | Comma separator                                    |
| `=`           | Terminal    | Equality operator                                  |
| `<>`          | Terminal    | Not equal operator                                 |
| `<`           | Terminal    | Less than operator                                 |
| `>`           | Terminal    | Greater than operator                              |
| `<=`          | Terminal    | Less than or equal operator                        |
| `>=`          | Terminal    | Greater than or equal operator                     |
| `identifier`  | Terminal    | Represents table or column names                  |
| `number`      | Terminal    | Numeric literals                                   |
| `string`      | Terminal    | String literals                                    |
| `;`           | Terminal    | Statement terminator                               |
| `<stmt>`      | Non-Terminal| The start symbol for a statement                   |
| `<select_stmt>`| Non-Terminal| Represents a SELECT statement                     |
| `<select_list>`| Non-Terminal| List of columns to select                         |
| `<column_list>`| Non-Terminal| List of individual columns                        |
| `<column>`     | Non-Terminal| Single column identifier                           |
| `<table_list>` | Non-Terminal| List of tables to select from                     |
| `<table>`      | Non-Terminal| Single table identifier                            |
| `<condition>`  | Non-Terminal| WHERE clause condition                             |
| `<expression>` | Non-Terminal| Expression within WHERE clause                     |
| `<operator>`   | Non-Terminal| Operators used in expressions                      |
| `<value>`      | Non-Terminal| Values in expressions (number or string)           |

---

## 5. Parse Table

The **Parse Table** is a table-driven method for syntax analysis. For simplicity, we'll use an LL(1) parse table based on our grammar.

### Columns: Terminals
`SELECT`, `FROM`, `WHERE`, `*`, `,`, `=`, `<>`, `<`, `>`, `<=`, `>=`, `identifier`, `number`, `string`, `;`, `EOF`

### Rows: Non-Terminals
`<stmt>`, `<select_stmt>`, `<select_list>`, `<column_list>`, `<column>`, `<table_list>`, `<table>`, `<condition>`, `<expression>`, `<operator>`, `<value>`

### Parse Table Entries

| Non-Terminal    | SELECT                              | FROM | WHERE | *                      | ,                  | = | <> | < | > | <= | >= | identifier                                | number | string | ;      | EOF  |
|-----------------|-------------------------------------|------|-------|------------------------|--------------------|---|----|---|---|----|----|--------------------------------------------|--------|--------|--------|------|
| `<stmt>`        | `<select_stmt>`                     |      |       |                        |                    |   |    |   |   |    |    |                                            |        |        |        |      |
| `<select_stmt>` | `SELECT <select_list> FROM <table_list> <opt_where>` |      |       |                        |                    |   |    |   |   |    |    |                                            |        |        |        |      |
| `<opt_where>`   |                                     |      | `WHERE <condition>` |                        |                    |   |    |   |   |    |    |                                            |        |        | `ε`    | `ε`  |
| `<select_list>` | `*` |      |       | `*`                      | `identifier`       |   |    |   |   |    |    | `identifier`                                |        |        |        |      |
| `<column_list>` |                                     |      |       |                        | `<column> , <column_list>` |   |    |   |   |    |    | `<column>`                                 |        |        |        |      |
| `<column>`      |                                     |      |       |                        | `identifier`       |   |    |   |   |    |    | `identifier`                                |        |        |        |      |
| `<table_list>`  |                                     |      |       |                        | `<table> , <table_list>` |   |    |   |   |    |    | `<table>`                                   |        |        |        |      |
| `<table>`       |                                     |      |       |                        | `identifier`       |   |    |   |   |    |    | `identifier`                                |        |        |        |      |
| `<condition>`   |                                     |      |       |                        |                    |   |    |   |   |    |    | `<expression>`                              |        |        |        |      |
| `<expression>`  |                                     |      |       |                        |                    |   |    |   |   |    |    | `<column> <operator> <value>`              |        |        |        |      |
| `<operator>`    |                                     |      |       |                        |                    | `=` | `<>` | `<` | `>` | `<=` | `>=` |                                            |        |        |        |      |
| `<value>`       |                                     |      |       |                        |                    |   |    |   |   |    |    | `number` | `string` |        |      |

**Notes**:
- `ε` represents an epsilon (empty) production.
- The table is partially filled to illustrate the structure. A complete table would include all 
possible productions for each non-terminal and terminal combination.
- `<opt_where>` is an optional production to handle the presence or absence of the `WHERE` clause.

### Example Parse Steps

Let's parse the SQL statement:

```sql
SELECT name, age FROM users WHERE age >= 18;
```

**Steps**:

1. **Start** with `<stmt>`.

2. `<stmt>` → `<select_stmt>`

3. `<select_stmt>` → `SELECT <select_list> FROM <table_list> <opt_where>`

4. `SELECT` matches `SELECT`.

5. `<select_list>` → `<column_list>`

6. `<column_list>` → `<column> , <column_list>`

7. `<column>` → `identifier` (`name`)

8. `,` matches `,`.

9. `<column_list>` → `<column>`

10. `<column>` → `identifier` (`age`)

11. `FROM` matches `FROM`.

12. `<table_list>` → `<table>`

13. `<table>` → `identifier` (`users`)

14. `<opt_where>` → `WHERE <condition>`

15. `WHERE` matches `WHERE`.

16. `<condition>` → `<expression>`

17. `<expression>` → `<column> <operator> <value>`

18. `<column>` → `identifier` (`age`)

19. `<operator>` → `>=`

20. `<value>` → `number` (`18`)

21. `;` matches `;`.

**Successful Parse**.

---

## Expanding to Full SQL

To cover every SQL scenario, consider the following steps:

1. **Expand the Grammar**: Incorporate additional SQL features such as `JOIN`, `GROUP BY`, `ORDER BY`, `INSERT`, `UPDATE`, 
`DELETE`, subqueries, functions, and more.

2. **Compute First & Follow Sets**: For the expanded grammar, compute First and Follow sets for all non-terminals. 
Tools like parser generators (e.g., ANTLR, YACC) can automate this.

3. **Populate the Parse Table**: Based on the expanded First & Follow sets and grammar, fill out the parse table accordingly.
 This requires meticulous attention to handle all possible terminal and non-terminal combinations.

4. **Build the Symbol Table**: Extend the symbol table to include data types, scope information, 
and other attributes relevant to SQL semantics.

5. **Handle Ambiguities**: Resolve any grammar ambiguities, possibly by refactoring the grammar or using parser generator directives.

6. **Automate with Tools**: Given the complexity, using parser generators like **ANTLR**, **Bison**, or 
**JavaCC** can significantly streamline the process. These tools can generate First & Follow sets, parse tables, and even the parser code itself.

---

## Conclusion

While the above example provides a foundational structure for parsing simple SQL `SELECT` statements, 
a full-fledged SQL compiler requires handling a vast array of syntax rules and scenarios. 
Leveraging parser generators and incremental grammar expansion will facilitate managing this complexity. 
If you need further assistance with specific SQL features or using parser tools, feel free to ask!
'''