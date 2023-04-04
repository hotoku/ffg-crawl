((python-mode
  . ((eval . (setq-local lsp-file-watch-ignored-directories
                         (cons "[/\\\\]\\.scrapy\\'" lsp-file-watch-ignored-directories))))))
