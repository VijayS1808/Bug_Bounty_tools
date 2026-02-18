curl -s "$1" | \
grep -Eoi '(href|src)=["'\'']?([^"'\'' >]+)' | \
sed -E 's/^(href|src)=["'\'']?//g' | \
awk '
/^https?:\/\// {print; next}
 /^\// {print $1$0; next}
 {print $1"/"$0}
' | sort -u
