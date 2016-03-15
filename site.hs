{-# LANGUAGE OverloadedStrings #-}
--import Control.Applicative ((<$>))
--import HakyllBibTex
import Data.Monoid (mappend, (<>))
import Hakyll
import System.Directory
import System.Process





-- There are a few limitations to the Vroom compiler
-- and I have not been able to get it working inside
-- the Hakyll compiler system. This is a very elementary
-- compilation process for Vroom slides.

--------------------------------------------------------------------------------
main :: IO ()


main = do

  
  hakyll $ do

    match "images/*" $ do
        route   idRoute
        compile copyFileCompiler

    match "css/*" $ do
        route   idRoute
        compile compressCssCompiler

    match "js/*" $ do
        route   idRoute
        compile copyFileCompiler

    match "*.bib" $ do
        route   idRoute
        compile copyFileCompiler

    tags <- buildTags "blog/posts/*" (fromCapture "tags/*.html")
    tagsRules tags $ \tag pattern -> do
        let title = "Posts tagged \"" ++ tag ++ "\""
        route idRoute
        compile $ do
            posts <- recentFirst =<< loadAllSnapshots pattern "content"
            let ctx = constField "title" title <>
                      listField "posts" (postCtx <> teaserField "teaser" "content") (return posts) <>
                      tagsCtx tags
            makeItem ""
                -- Use a more simple post-list template for this.
                >>= loadAndApplyTemplate "templates/blog.html" ctx
                >>= loadAndApplyTemplate "templates/default.html" ctx
                >>= relativizeUrls

    match (fromList ["publication.html","Contact.html","People.html","Software.html","Publications.html"]) $ do
         route idRoute
         compile $ copyFileCompiler
         compile $ pandocCompiler
             >>= loadAndApplyTemplate "templates/default.html" defaultContext
             >>= relativizeUrls


          
    match (fromList ["about.markdown", "services.markdown","projects.markdown",
                  "portfolio.markdown", "education.markdown","members.markdown",
                     "talks.markdown"]) $ do
        route   $ setExtension "html"
        compile $ pandocCompiler
            >>= loadAndApplyTemplate "templates/default.html" defaultContext
            >>= relativizeUrls

    match "blog/posts/*" $ do
        route $ setExtension "html"
        compile $ pandocCompiler
            >>= saveSnapshot "content"
            >>= loadAndApplyTemplate "templates/post.html" (tagsCtx tags)
            >>= saveSnapshot "atom"
            >>= loadAndApplyTemplate "templates/default.html" postCtx
            >>= relativizeUrls



    match "index.html" $ do
        route idRoute
        compile $ do
            posts <- fmap (take 5) . recentFirst =<< loadAll "blog/posts/*"
            let indexCtx =
                    listField "posts" postCtx (return posts) `mappend`
                    constField "title" "University of Utah Parallelism"  `mappend`
                    defaultContext

            getResourceBody
                >>= applyAsTemplate indexCtx
                >>= loadAndApplyTemplate "templates/default.html" indexCtx
                >>= relativizeUrls

    match "templates/*" $ compile templateCompiler
  where
    dropEnd n = reverse . drop n . reverse

--------------------------------------------------------------------------------
tagsCtx :: Tags -> Context String
tagsCtx tags = field "taglist" (\_ -> renderTagList tags) <>
               tagsField "tags" tags <>
               postCtx

postCtx :: Context String
postCtx =
    dateField "date" "%B %e, %Y" `mappend`
    defaultContext
