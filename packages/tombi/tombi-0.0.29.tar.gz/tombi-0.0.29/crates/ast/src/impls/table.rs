use crate::{support, ArrayOfTables, AstChildren, AstNode, TableOrArrayOfTable};
use config::TomlVersion;
use syntax::T;

impl crate::Table {
    pub fn header_leading_comments(&self) -> impl Iterator<Item = crate::Comment> {
        support::node::leading_comments(self.syntax().children_with_tokens())
    }

    pub fn header_tailing_comment(&self) -> Option<crate::Comment> {
        support::node::tailing_comment(self.syntax().children_with_tokens(), T!(']'))
    }

    /// Returns an iterator over the subtables of this table.
    ///
    /// ```toml
    /// [foo]  # <- This is a self table
    /// [foo.bar]  # <- This is a subtable
    /// key = "value"
    ///
    /// [[foo.bar.baz]]  # <- This is also a subtable
    /// key = true
    /// ```
    pub fn subtables<'a>(&'a self) -> impl Iterator<Item = TableOrArrayOfTable> + 'a {
        support::node::next_siblings_nodes(self).take_while(|t: &TableOrArrayOfTable| {
            t.header()
                .unwrap()
                .keys()
                .starts_with(&self.header().unwrap().keys())
        })
    }

    pub fn array_of_tables_keys<'a>(
        &'a self,
    ) -> impl Iterator<Item = AstChildren<crate::Key>> + 'a {
        support::node::prev_siblings_nodes(self)
            .map(|node: ArrayOfTables| node.header().unwrap().keys())
            .take_while(
                |keys| match (self.header().unwrap().keys().next(), keys.clone().next()) {
                    (Some(a), Some(b)) => match (
                        a.try_to_raw_text(TomlVersion::latest()),
                        b.try_to_raw_text(TomlVersion::latest()),
                    ) {
                        (Ok(a), Ok(b)) => a == b,
                        _ => false,
                    },
                    _ => false,
                },
            )
            .filter(|keys| self.header().unwrap().keys().starts_with(&keys))
    }
}
