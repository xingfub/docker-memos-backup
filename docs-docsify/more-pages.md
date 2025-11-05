# 多页文档

如果你需要多个页面，你可以在你的 docsify 目录中创建更多的 markdown 文件。 如果创建了名为 `guide.md` 的文件，则可通过 `/#/guide` 访问该文件。

假设你的目录结构如下：

```text
.
└── docs
    ├── README.md
    ├── guide.md
    └── zh-cn
        ├── README.md
        └── guide.md
```

对应的访问页面路由将是

```text
docs/README.md        => http://domain.com
docs/guide.md         => http://domain.com/#/guide
docs/zh-cn/README.md  => http://domain.com/#/zh-cn/
docs/zh-cn/guide.md   => http://domain.com/#/zh-cn/guide
```

## 侧边栏

为了拥有侧边栏，你可以创建自己的 `_sidebar.md`（示例参见[本文档的侧边栏](https://github.com/docsifyjs/docs-zh/blob/main/_sidebar.md?plain=1)）：

首先，需要将 `loadSidebar` 设置为 **true**。 详细信息请参阅[配置段落](zh-cn/configuration#loadsidebar)。

```html
<!-- index.html -->

<script>
  window.$docsify = {
    loadSidebar: true,
  };
</script>
<script src="//cdn.jsdelivr.net/npm/docsify@5/dist/docsify.min.js"></script>
```

创建 `_sidebar.md`：

```markdown
<!-- docs/_sidebar.md -->

- [Home](/)
- [Guide](guide.md)
```

需要在 `./docs` 目录创建 `.nojekyll` 命名的空文件，阻止 GitHub Pages 忽略命名是下划线开头的文件。

!> Docsify 只查找当前文件夹中的 `_sidebar.md`，并使用它，否则会返回到使用 `window.$docsify.loadSidebar` 配置。

示例文件结构：

```text
└── docs/
    ├── _sidebar.md
    ├── index.md
    ├── getting-started.md
    └── running-services.md
```

## 嵌套侧边栏

你可能想要浏览到一个目录时，只显示这个目录自己的侧边栏。 这可以通过在每个文件夹中添加一个 `_sidebar.md` 文件来实现。

`_sidebar.md`会从每一级目录加载。 如果当前目录中没有 `_sidebar.md`，则会返回上一级目录。 例如如果当前路径是 `/guide/quick-start`，则 `_sidebar.md` 将从 `/guide/_sidebar.md` 加载。

你也可以配置 `alias` 避免不必要的回退过程。

```html
<script>
  window.$docsify = {
    loadSidebar: true,
    alias: {
      '/.*/_sidebar.md': '/_sidebar.md',
    },
  };
</script>
```

!> 你可以在一个子目录中创建一个 `README.md` 文件来作为路由的默认网页。

## 用侧边栏中选定的条目名称作为页面标题

一个页面的 `title` 标签是由侧边栏中_选中_条目的名称所生成的。 为了更好的 SEO ，你可以在文件名后面指定页面标题。

```markdown
<!-- docs/_sidebar.md -->

- [Home](/)
- [Guide](guide.md 'The greatest guide in the world')
```

## 目录

创建 `_sidebar.md` 后，侧边栏内容就会根据 markdown 文件中的标题自动生成。

自定义侧边栏还可以通过设置 `subMaxLevel` 自动生成目录，参考 [subMaxLevel 配置](zh-cn/configuration#submaxlevel)。

```html
<!-- index.html -->

<script>
  window.$docsify = {
    loadSidebar: true,
    subMaxLevel: 2,
  };
</script>
<script src="//cdn.jsdelivr.net/npm/docsify@5/dist/docsify.min.js"></script>
```

## 忽略副标题

当设置了 `subMaxLevel` 时，默认情况下每个标题都会自动添加到目录中。 如果要忽略某个特定的标题，请添加 `<!-- {docsify-ignore} -->`。

```markdown
# Getting Started

## Header <!-- {docsify-ignore} -->

该标题不会出现在侧边栏的目录中。
```

要忽略特定页面上的所有标题，你可以在页面的第一个标题上使用 `<!-- {docsify-ignore-all} -->` 。

```markdown
# Getting Started <!-- {docsify-ignore-all} -->

## Header

该标题不会出现在侧边栏的目录中。
```

在使用时， `<!-- {docsify-ignore} -->` 和 `<!-- {docsify-ignore-all} -->` 都不会在页面上呈现。

{docsify-ignore} 和 {docsify-ignore-all} 也可以做同样的事情。
