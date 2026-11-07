def read_elements():
    elements = []
    with open("periodic_table.txt", encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            name, attributes = line.split("=", 1)
            element = {"name": name.strip()}
            for attribute in attributes.split(","):
                key, value = attribute.split(":", 1)
                element[key.strip()] = value.strip()
            elements.append(element)
    return elements


def escape_html(value):
    return (value.replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def make_rows(elements):
    rows = []
    previous_position = 17
    for element in elements:
        position = int(element["position"])
        if position <= previous_position:
            rows.append([None] * 18)
        rows[-1][position] = element
        previous_position = position
    return rows


def render_element(element):
    if element is None:
        return '          <td class="empty"></td>'
    return "\n".join([
        "          <td>",
        "            <h4>" + escape_html(element["name"]) + "</h4>",
        "            <ul>",
        "              <li>Atomic number: " + escape_html(element["number"]) + "</li>",
        "              <li>Symbol: " + escape_html(element["small"]) + "</li>",
        "              <li>Atomic mass: " + escape_html(element["molar"]) + "</li>",
        "              <li>Electrons: " + escape_html(element["electron"]) + "</li>",
        "            </ul>",
        "          </td>"
    ])


def periodic_table():
    rows = make_rows(read_elements())
    document = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        "  <title>Periodic table of the elements</title>",
        "  <style>",
        "    body { font-family: sans-serif; margin: 24px; color: #172033; }",
        "    .table-container { overflow-x: auto; }",
        "    table { border-collapse: collapse; table-layout: fixed; width: 2160px; }",
        "    caption { text-align: left; margin-bottom: 16px; }",
        "    td { border: 1px solid #64748b; padding: 8px; vertical-align: top;",
        "         background: #eff6ff; overflow-wrap: anywhere; }",
        "    td.empty { border: 0; background: transparent; }",
        "    h4 { margin: 0 0 10px; font-size: 13px; }",
        "    ul { list-style: none; margin: 0; padding: 0; font-size: 12px; }",
        "    li { margin-bottom: 6px; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <main>",
        "    <h1>Periodic table of the elements</h1>",
        "    <h2>Element properties</h2>",
        "    <h3>By period and group</h3>",
        '    <div class="table-container">',
        "      <table>",
        "        <caption>Atomic number, symbol, atomic mass and electron configuration</caption>",
        "        <tbody>"
    ]
    for row in rows:
        document.append("        <tr>")
        for element in row:
            document.append(render_element(element))
        document.append("        </tr>")
    document.extend([
        "        </tbody>",
        "      </table>",
        "    </div>",
        "  </main>",
        "</body>",
        "</html>"
    ])
    with open("periodic_table.html", "w", encoding="utf-8") as output:
        output.write("\n".join(document) + "\n")


if __name__ == '__main__':
    periodic_table()
