import os
import langchain
import pkgutil

print(f"Langchain path: {langchain.__path__}")
print(f"Langchain dir: {dir(langchain)}")

# List submodules
package_path = langchain.__path__[0]
print(f"Contents of {package_path}:")
try:
    print(os.listdir(package_path))
except Exception as e:
    print(f"Error listing dir: {e}")

# Try to find RetrievalQA
print("\nSearching for RetrievalQA...")
# It might be in langchain.chains (which might be missing) or langchain_community

try:
    import langchain.chains
    print("Imported langchain.chains")
except ImportError as e:
    print(f"Could not import langchain.chains: {e}")

try:
    from langchain_community.chains import RetrievalQA
    print("Found RetrievalQA in langchain_community.chains")
except ImportError:
    print("Not in langchain_community.chains")

try:
    from langchain.chains import RetrievalQA
    print("Found RetrievalQA in langchain.chains")
except ImportError:
    print("Not in langchain.chains")
